
codeunit 50110 "MX Sync"
{
    procedure SynchroniseAssessments(ApiBaseUrl: Text)
    var
        ApiClient: Codeunit "MX API Client";
        JsonParser: Codeunit "MX JSON Parser";
        Assessment: Record "MX Health Assessment";
        Equipment: Record "MX Equipment";
        JsonArray: JsonArray;
        JsonToken: JsonToken;
        JsonObject: JsonObject;
        AssessmentId: Guid;
        EquipmentId: Guid;
        ComponentId: Guid;
        AssessmentType: Code[30];
        Condition: Enum "MX Equipment Condition";
        FindingCount: Integer;
        ImportedFindingCount: Integer;
        Recommendation: Text[1000];
        AssessedAt: DateTime;
        ResponseText: Text;
        ErrorMessage: Text;
        ImportedCount: Integer;
        SkippedCount: Integer;
        Index: Integer;
        AssessmentEntryNo: Integer;
    begin
        if not ApiClient.GetAssessments(ApiBaseUrl, ResponseText, ErrorMessage) then
            Error(ErrorMessage);

        if not JsonArray.ReadFrom(ResponseText) then
            Error('The MAINTAINX API returned invalid JSON.');

        for Index := 0 to JsonArray.Count() - 1 do begin
            if not JsonArray.Get(Index, JsonToken) then
                Error('Unable to read assessment at position %1.', Index + 1);

            if not JsonToken.IsObject() then
                Error('Assessment at position %1 is not a valid JSON object.', Index + 1);

            JsonObject := JsonToken.AsObject();

            if not JsonParser.ParseAssessment(
                JsonObject,
                AssessmentId,
                EquipmentId,
                ComponentId,
                AssessmentType,
                Condition,
                FindingCount,
                Recommendation,
                AssessedAt
            ) then
                Error('Unable to parse assessment at position %1.', Index + 1);

            if AssessmentAlreadyImported(AssessmentId) then begin
                SkippedCount += 1;
                continue;
            end;

            Equipment.Reset();
            Equipment.SetRange("MAINTAINX Equipment ID", EquipmentId);

            if not Equipment.FindFirst() then
                Error(
                    'No matching Business Central equipment record exists for MAINTAINX equipment ID %1.',
                    EquipmentId
                );

            Assessment.Init();
            Assessment."MAINTAINX Assessment ID" := AssessmentId;
            Assessment."MAINTAINX Equipment ID" := EquipmentId;
            Assessment."MAINTAINX Component ID" := ComponentId;
            Assessment."Equipment Code" := Equipment."Equipment Code";
            Assessment."Assessment Type" := AssessmentType;
            Assessment.Condition := Condition;
            Assessment."Finding Count" := FindingCount;
            Assessment.Recommendation := Recommendation;
            Assessment."Assessed At" := AssessedAt;
            Assessment.Insert(true);

            AssessmentEntryNo := Assessment."Entry No.";

            if not JsonObject.Get('findings', JsonToken) then
                Error(
                    'Assessment %1 does not contain a findings collection.',
                    AssessmentId
                );

            ImportedFindingCount := ImportFindings(
                JsonToken,
                AssessmentEntryNo,
                FindingCount,
                JsonParser
            );

            if ImportedFindingCount <> FindingCount then
                Error(
                    'Finding count mismatch for assessment %1. Expected %2, imported %3.',
                    AssessmentId,
                    FindingCount,
                    ImportedFindingCount
                );

            ImportedCount += 1;
        end;

        Message(
            'MAINTAINX synchronisation completed.\Imported assessments: %1\Skipped assessments: %2',
            ImportedCount,
            SkippedCount
        );
    end;

    local procedure ImportFindings(
        FindingsToken: JsonToken;
        AssessmentEntryNo: Integer;
        ExpectedFindingCount: Integer;
        var JsonParser: Codeunit "MX JSON Parser"
    ): Integer
    var
        Finding: Record "MX Assessment Finding";
        FindingsArray: JsonArray;
        FindingToken: JsonToken;
        FindingObject: JsonObject;
        SensorType: Code[50];
        Severity: Enum "MX Equipment Condition";
        MeasuredValue: Decimal;
        Unit: Text[20];
        FindingMessage: Text[250];
        ImportedFindingCount: Integer;
        Index: Integer;
    begin
        if not FindingsToken.IsArray() then
            Error('The assessment findings property is not a JSON array.');

        FindingsArray := FindingsToken.AsArray();

        if FindingsArray.Count() <> ExpectedFindingCount then
            Error(
                'Expected %1 findings but received %2.',
                ExpectedFindingCount,
                FindingsArray.Count()
            );

        for Index := 0 to FindingsArray.Count() - 1 do begin
            if not FindingsArray.Get(Index, FindingToken) then
                Error('Unable to read finding at position %1.', Index + 1);

            if not FindingToken.IsObject() then
                Error('Finding at position %1 is not a valid JSON object.', Index + 1);

            FindingObject := FindingToken.AsObject();

            if not JsonParser.ParseFinding(
                FindingObject,
                SensorType,
                Severity,
                MeasuredValue,
                Unit,
                FindingMessage
            ) then
                Error('Unable to parse finding at position %1.', Index + 1);

            Finding.Init();
            Finding."Assessment Entry No." := AssessmentEntryNo;
            Finding."Sensor Type" := SensorType;
            Finding.Severity := Severity;
            Finding."Measured Value" := MeasuredValue;
            Finding.Unit := Unit;
            Finding.Message := FindingMessage;
            Finding.Insert(true);

            ImportedFindingCount += 1;
        end;

        exit(ImportedFindingCount);
    end;

    local procedure AssessmentAlreadyImported(AssessmentId: Guid): Boolean
    var
        Assessment: Record "MX Health Assessment";
    begin
        Assessment.Reset();
        Assessment.SetRange("MAINTAINX Assessment ID", AssessmentId);
        exit(not Assessment.IsEmpty());
    end;
}
