
table 50100 "MX Equipment"
{
    Caption = 'MAINTAINX Equipment';
    DataClassification = CustomerContent;

    fields
    {
        field(1; "Entry No."; Integer)
        {
            Caption = 'Entry No.';
            DataClassification = SystemMetadata;
            AutoIncrement = true;
        }

        field(2; "Equipment Code"; Code[30])
        {
            Caption = 'Equipment Code';
            DataClassification = CustomerContent;
            NotBlank = true;
        }

        field(3; "Equipment Name"; Text[100])
        {
            Caption = 'Equipment Name';
            DataClassification = CustomerContent;
        }

        field(4; "Equipment Type"; Text[50])
        {
            Caption = 'Equipment Type';
            DataClassification = CustomerContent;
        }

        field(5; Manufacturer; Text[100])
        {
            Caption = 'Manufacturer';
            DataClassification = CustomerContent;
        }

        field(6; Model; Text[50])
        {
            Caption = 'Model';
            DataClassification = CustomerContent;
        }

        field(7; Site; Text[100])
        {
            Caption = 'Site';
            DataClassification = CustomerContent;
        }

        field(8; "MAINTAINX Equipment ID"; Guid)
        {
            Caption = 'MAINTAINX Equipment ID';
            DataClassification = CustomerContent;
        }

        field(9; Status; Text[30])
        {
            Caption = 'Status';
            DataClassification = CustomerContent;
        }
    }

    keys
    {
        key(PK; "Entry No.")
        {
            Clustered = true;
        }

        key(EquipmentCode; "Equipment Code")
        {
            Unique = true;
        }
    }
}
