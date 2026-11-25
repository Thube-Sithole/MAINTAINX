
page 50102 "MX Equipment Card"
{
    Caption = 'MAINTAINX Equipment Card';
    PageType = Card;
    SourceTable = "MX Equipment";
    ApplicationArea = All;
    UsageCategory = None;

    layout
    {
        area(Content)
        {
            group(General)
            {
                Caption = 'Equipment Information';

                field("Entry No."; Rec."Entry No.")
                {
                    ApplicationArea = All;
                    Editable = false;
                }

                field("Equipment Code"; Rec."Equipment Code")
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies the unique equipment code.';
                }

                field("Equipment Name"; Rec."Equipment Name")
                {
                    ApplicationArea = All;
                }

                field("Equipment Type"; Rec."Equipment Type")
                {
                    ApplicationArea = All;
                }

                field(Manufacturer; Rec.Manufacturer)
                {
                    ApplicationArea = All;
                }

                field(Model; Rec.Model)
                {
                    ApplicationArea = All;
                }

                field(Site; Rec.Site)
                {
                    ApplicationArea = All;
                }

                field(Status; Rec.Status)
                {
                    ApplicationArea = All;
                }
            }

            group(Integration)
            {
                Caption = 'MAINTAINX Integration';

                field("MAINTAINX Equipment ID"; Rec."MAINTAINX Equipment ID")
                {
                    ApplicationArea = All;
                    Editable = false;
                    ToolTip = 'Specifies the corresponding equipment identifier in MAINTAINX.';
                }
            }
        }
    }

    actions
    {
        area(Processing)
        {
            action(ViewAssessments)
            {
                Caption = 'View Health Assessments';
                ApplicationArea = All;
                Image = History;

                RunObject = page "MX Assessment List";
                RunPageLink = "Equipment Code" = field("Equipment Code");
                RunPageMode = View;

                ToolTip = 'View predictive health assessments for this equipment.';
            }
        }
    }
}
