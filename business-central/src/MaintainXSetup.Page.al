
page 50114 "MX Setup"
{
    Caption = 'MAINTAINX Setup';
    PageType = Card;
    SourceTable = "MX Setup";
    ApplicationArea = All;
    UsageCategory = Administration;

    layout
    {
        area(Content)
        {
            group(General)
            {
                Caption = 'Integration Settings';

                field("API Base URL"; Rec."API Base URL")
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies the base URL of the MAINTAINX predictive intelligence API.';
                }

                field("API Enabled"; Rec."API Enabled")
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies whether the MAINTAINX integration is enabled.';
                }
            }

            group(Synchronisation)
            {
                Caption = 'Synchronisation Status';

                field("Last Sync DateTime"; Rec."Last Sync DateTime")
                {
                    ApplicationArea = All;
                    Editable = false;
                }

                field("Last Sync Status"; Rec."Last Sync Status")
                {
                    ApplicationArea = All;
                    Editable = false;
                }
            }
        }
    }

    actions
    {
        area(Processing)
        {
            action(SynchroniseAssessments)
            {
                Caption = 'Synchronise Assessments';
                ApplicationArea = All;
                Image = Refresh;
                ToolTip = 'Retrieve predictive health assessments from MAINTAINX.';

                trigger OnAction()
                var
                    SyncCodeunit: Codeunit "MX Sync";
                begin
                    if not Rec."API Enabled" then
                        Error('The MAINTAINX integration is not enabled.');

                    if Rec."API Base URL" = '' then
                        Error('Enter the MAINTAINX API base URL first.');

                    SyncCodeunit.SynchroniseAssessments(Rec."API Base URL");

                    Rec."Last Sync DateTime" := CurrentDateTime();
                    Rec."Last Sync Status" := 'Completed';
                    Rec.Modify(true);

                    CurrPage.Update(false);
                end;
            }
        }
    }

    trigger OnOpenPage()
    begin
        if not Rec.Get('DEFAULT') then begin
            Rec.Init();
            Rec."Primary Key" := 'DEFAULT';
            Rec."API Base URL" := 'http://127.0.0.1:8000';
            Rec.Insert(true);
        end;
    end;
}
