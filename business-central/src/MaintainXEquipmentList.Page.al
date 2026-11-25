
page 50101 "MX Equipment List"
{
    Caption = 'MAINTAINX Equipment';
    PageType = List;
    SourceTable = "MX Equipment";
    ApplicationArea = All;
    UsageCategory = Lists;

    CardPageId = "MX Equipment Card";

    layout
    {
        area(Content)
        {
            repeater(General)
            {
                field("Equipment Code"; Rec."Equipment Code")
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies the equipment identification code.';
                }

                field("Equipment Name"; Rec."Equipment Name")
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies the equipment name.';
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
        }
    }
}
