
page 50112 "MX Assessment Findings"
{
    Caption = 'MAINTAINX Assessment Findings';
    PageType = ListPart;
    SourceTable = "MX Assessment Finding";
    ApplicationArea = All;

    layout
    {
        area(Content)
        {
            repeater(General)
            {
                field("Sensor Type"; Rec."Sensor Type")
                {
                    ApplicationArea = All;
                }

                field(Severity; Rec.Severity)
                {
                    ApplicationArea = All;
                }

                field("Measured Value"; Rec."Measured Value")
                {
                    ApplicationArea = All;
                }

                field(Unit; Rec.Unit)
                {
                    ApplicationArea = All;
                }

                field(Message; Rec.Message)
                {
                    ApplicationArea = All;
                }
            }
        }
    }
}
