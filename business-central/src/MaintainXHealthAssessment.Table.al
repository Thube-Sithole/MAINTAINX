
table 50103 "MX Health Assessment"
{
    Caption = 'MAINTAINX Health Assessment';
    DataClassification = CustomerContent;

    fields
    {
        field(1; "Entry No."; Integer)
        {
            Caption = 'Entry No.';
            DataClassification = SystemMetadata;
            AutoIncrement = true;
        }

        field(2; "MAINTAINX Assessment ID"; Guid)
        {
            Caption = 'MAINTAINX Assessment ID';
            DataClassification = CustomerContent;
        }

        field(3; "MAINTAINX Equipment ID"; Guid)
        {
            Caption = 'MAINTAINX Equipment ID';
            DataClassification = CustomerContent;
        }

        field(4; "MAINTAINX Component ID"; Guid)
        {
            Caption = 'MAINTAINX Component ID';
            DataClassification = CustomerContent;
        }

        field(5; "Equipment Code"; Code[30])
        {
            Caption = 'Equipment Code';
            DataClassification = CustomerContent;
            TableRelation = "MX Equipment"."Equipment Code";
        }

        field(6; "Assessment Type"; Code[30])
        {
            Caption = 'Assessment Type';
            DataClassification = CustomerContent;
        }

        field(7; Condition; Enum "MX Equipment Condition")
        {
            Caption = 'Overall Condition';
            DataClassification = CustomerContent;
        }

        field(8; "Finding Count"; Integer)
        {
            Caption = 'Finding Count';
            DataClassification = CustomerContent;
        }

        field(9; Recommendation; Text[1000])
        {
            Caption = 'Recommendation';
            DataClassification = CustomerContent;
        }

        field(10; "Assessed At"; DateTime)
        {
            Caption = 'Assessed At';
            DataClassification = CustomerContent;
        }
    }

    keys
    {
        key(PK; "Entry No.")
        {
            Clustered = true;
        }

        key(AssessmentId; "MAINTAINX Assessment ID")
        {
            Unique = true;
        }

        key(EquipmentCode; "Equipment Code", "Assessed At")
        {
        }
    }
}
