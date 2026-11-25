
codeunit 50109 "MX JSON Parser"
{
    procedure ParseAssessment(
        JsonObject: JsonObject;
        var AssessmentId: Guid;
        var EquipmentId: Guid;
        var ComponentId: Guid;
        var AssessmentType: Code[30];
        var Condition: Enum "MX Equipment Condition";
        var FindingCount: Integer;
        var Recommendation: Text[1000];
        var AssessedAt: DateTime
    ): Boolean
    var
        JsonToken: JsonToken;
        ConditionText: Text;
        AssessedAtText: Text;
    begin
        Clear(AssessmentId);
        Clear(EquipmentId);
        Clear(ComponentId);
        Clear(AssessmentType);
        Clear(Condition);
        Clear(FindingCount);
        Clear(Recommendation);
        Clear(AssessedAt);

        if not JsonObject.Get('id', JsonToken) then
            exit(false);

        if not Evaluate(AssessmentId, JsonToken.AsValue().AsText()) then
            exit(false);

        if not JsonObject.Get('equipment_id', JsonToken) then
            exit(false);

        if not Evaluate(EquipmentId, JsonToken.AsValue().AsText()) then
            exit(false);

        if not JsonObject.Get('component_id', JsonToken) then
            exit(false);

        if not Evaluate(ComponentId, JsonToken.AsValue().AsText()) then
            exit(false);

        if not JsonObject.Get('assessment_type', JsonToken) then
            exit(false);

        AssessmentType := CopyStr(
            JsonToken.AsValue().AsText(),
            1,
            MaxStrLen(AssessmentType)
        );

        if not JsonObject.Get('overall_condition', JsonToken) then
            exit(false);

        ConditionText := JsonToken.AsValue().AsText();

        case LowerCase(ConditionText) of
            'normal':
                Condition := Condition::Normal;
            'warning':
                Condition := Condition::Warning;
            'critical':
                Condition := Condition::Critical;
            else
                Condition := Condition::Unknown;
        end;

        if not JsonObject.Get('finding_count', JsonToken) then
            exit(false);

        FindingCount := JsonToken.AsValue().AsInteger();

        if not JsonObject.Get('recommendation', JsonToken) then
            exit(false);

        Recommendation := CopyStr(
            JsonToken.AsValue().AsText(),
            1,
            MaxStrLen(Recommendation)
        );

        if not JsonObject.Get('assessed_at', JsonToken) then
            exit(false);

        AssessedAtText := JsonToken.AsValue().AsText();

        if not Evaluate(AssessedAt, AssessedAtText) then
            exit(false);

        exit(true);
    end;

    procedure ParseFinding(
        JsonObject: JsonObject;
        var SensorType: Code[50];
        var Severity: Enum "MX Equipment Condition";
        var MeasuredValue: Decimal;
        var Unit: Text[20];
        var FindingMessage: Text[250]
    ): Boolean
    var
        JsonToken: JsonToken;
        SeverityText: Text;
    begin
        Clear(SensorType);
        Clear(Severity);
        Clear(MeasuredValue);
        Clear(Unit);
        Clear(FindingMessage);

        if not JsonObject.Get('sensor', JsonToken) then
            exit(false);

        SensorType := CopyStr(
            JsonToken.AsValue().AsText(),
            1,
            MaxStrLen(SensorType)
        );

        if not JsonObject.Get('severity', JsonToken) then
            exit(false);

        SeverityText := JsonToken.AsValue().AsText();

        case LowerCase(SeverityText) of
            'normal':
                Severity := Severity::Normal;
            'warning':
                Severity := Severity::Warning;
            'critical':
                Severity := Severity::Critical;
            else
                Severity := Severity::Unknown;
        end;

        if not JsonObject.Get('value', JsonToken) then
            exit(false);

        MeasuredValue := JsonToken.AsValue().AsDecimal();

        if not JsonObject.Get('unit', JsonToken) then
            exit(false);

        Unit := CopyStr(
            JsonToken.AsValue().AsText(),
            1,
            MaxStrLen(Unit)
        );

        if not JsonObject.Get('message', JsonToken) then
            exit(false);

        FindingMessage := CopyStr(
            JsonToken.AsValue().AsText(),
            1,
            MaxStrLen(FindingMessage)
        );

        exit(true);
    end;
}
