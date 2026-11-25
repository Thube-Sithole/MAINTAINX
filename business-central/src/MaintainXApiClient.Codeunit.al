
codeunit 50106 "MX API Client"
{
    procedure GetAssessments(
        ApiBaseUrl: Text;
        var ResponseText: Text;
        var ErrorMessage: Text
    ): Boolean
    var
        HttpClient: HttpClient;
        HttpResponse: HttpResponseMessage;
        ResponseContent: HttpContent;
        RequestUrl: Text;
    begin
        Clear(ResponseText);
        Clear(ErrorMessage);

        if ApiBaseUrl = '' then begin
            ErrorMessage := 'MAINTAINX API base URL has not been configured.';
            exit(false);
        end;

        // Remove trailing slash to prevent malformed URLs.
        RequestUrl := DelChr(ApiBaseUrl, '>', '/') + '/assessments/';

        // Send the HTTP GET request.
        if not HttpClient.Get(RequestUrl, HttpResponse) then begin
            ErrorMessage := 'Unable to connect to the MAINTAINX API.';
            exit(false);
        end;

        // Validate the HTTP response status.
        if not HttpResponse.IsSuccessStatusCode() then begin
            ErrorMessage := StrSubstNo(
                'MAINTAINX API returned HTTP status %1.',
                HttpResponse.HttpStatusCode()
            );

            exit(false);
        end;

        // Retrieve the response content.
        ResponseContent := HttpResponse.Content();

        if not ResponseContent.ReadAs(ResponseText) then begin
            ErrorMessage := 'Unable to read the MAINTAINX API response.';
            exit(false);
        end;

        exit(true);
    end;
}
