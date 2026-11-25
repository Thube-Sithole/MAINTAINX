
table 50104 "MX Assessment Finding"
{
    Caption = 'MAINTAINX Assessment Finding';
    DataClassification = CustomerContent;

    fields
    {
        field(1; "Entry No."; Integer)
        {
            Caption = 'Entry No.';
            DataClassification = SystemMetadata;
            AutoIncrement = true;
        }

        field(2; "Assessment Entry No."; Integer)
        {
            Caption = 'Assessment Entry No.';
            DataClassification = SystemMetadata;
            TableRelation = "MX Health Assessment"."Entry No.";
        }

        field(3; "Sensor Type"; Code[50])
        {
            Caption = 'Sensor Type';
            DataClassification = CustomerContent;
        }

        field(4; Severity; Enum "MX Equipment Condition")
        {
            Caption = 'Severity';
            DataClassification = CustomerContent;
        }

        field(5; "Measured Value"; Decimal)
        {
            Caption = 'Measured Value';
            DataClassification = CustomerContent;
            DecimalPlaces = 0 : 5;
        }

        field(6; Unit; Text[20])
        {
            Caption = 'Unit';
            DataClassification = CustomerContent;
        }

        field(7; Message; Text[250])
        {
            Caption = 'Finding Message';
            DataClassification = CustomerContent;
        }
    }

    keys
    {
        key(PK; "Entry No.")
        {
            Clustered = true;
        }

        key(Assessment; "Assessment Entry No.")
        {
        }
    }
}
