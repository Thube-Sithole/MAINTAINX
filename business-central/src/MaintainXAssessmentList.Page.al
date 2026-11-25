
page 50105 "MX Assessment List"
{
    Caption = 'MAINTAINX Health Assessments';
    PageType = List;
    SourceTable = "MX Health Assessment";
    ApplicationArea = All;
    UsageCategory = Lists;

    layout
    {
        area(Content)
        {
            repeater(General)
            {
                field("Equipment Code"; Rec."Equipment Code")
                {
                    ApplicationArea = All;
                }

                field("Assessment Type"; Rec."Assessment Type")
                {
                    ApplicationArea = All;
                }

                field(Condition; Rec.Condition)
                {
                    ApplicationArea = All;
                    StyleExpr = ConditionStyle;
                }

                field("Finding Count"; Rec."Finding Count")
                {
                    ApplicationArea = All;
                }

                field(Recommendation; Rec.Recommendation)
                {
                    ApplicationArea = All;
                }

                field("Assessed At"; Rec."Assessed At")
                {
                    ApplicationArea = All;
                }
            }
        }
    }

    var
        ConditionStyle: Text;

    trigger OnAfterGetRecord()
    begin
        case Rec.Condition of
            Rec.Condition::Normal:
                ConditionStyle := 'Favorable';
            Rec.Condition::Warning:
                ConditionStyle := 'Ambiguous';
            Rec.Condition::Critical:
                ConditionStyle := 'Unfavorable';
            else
                ConditionStyle := 'Standard';
        end;
    end;
}
