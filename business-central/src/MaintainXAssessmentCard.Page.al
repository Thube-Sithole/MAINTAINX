
page 50111 "MX Assessment Card"
{
    Caption = 'MAINTAINX Assessment Card';
    PageType = Card;
    SourceTable = "MX Health Assessment";
    ApplicationArea = All;
    UsageCategory = None;

    layout
    {
        area(Content)
        {
            group(General)
            {
                Caption = 'Assessment Information';

                field("MAINTAINX Assessment ID"; Rec."MAINTAINX Assessment ID")
                {
                    ApplicationArea = All;
                    Editable = false;
                }

                field("Equipment Code"; Rec."Equipment Code")
                {
                    ApplicationArea = All;
                    Editable = false;
                }

                field("Assessment Type"; Rec."Assessment Type")
                {
                    ApplicationArea = All;
                    Editable = false;
                }

                field(Condition; Rec.Condition)
                {
                    ApplicationArea = All;
                    Editable = false;
                }

                field("Finding Count"; Rec."Finding Count")
                {
                    ApplicationArea = All;
                    Editable = false;
                }

                field("Assessed At"; Rec."Assessed At")
                {
                    ApplicationArea = All;
                    Editable = false;
                }
            }

            group(Recommendation)
            {
                Caption = 'Engineering Recommendation';

                field(RecommendationText; Rec.Recommendation)
                {
                    ApplicationArea = All;
                    Editable = false;
                    MultiLine = true;
                    ShowCaption = false;
                }
            }

            part(AssessmentFindings; "MX Assessment Findings")
            {
                ApplicationArea = All;
                SubPageLink = "Assessment Entry No." = field("Entry No.");
            }
        }
    }
}
