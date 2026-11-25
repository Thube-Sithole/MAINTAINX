
table 50113 "MX Setup"
{
    Caption = 'MAINTAINX Setup';
    DataClassification = CustomerContent;

    fields
    {
        field(1; "Primary Key"; Code[10])
        {
            Caption = 'Primary Key';
            DataClassification = SystemMetadata;
        }

        field(2; "API Base URL"; Text[250])
        {
            Caption = 'API Base URL';
            DataClassification = CustomerContent;
        }

        field(3; "API Enabled"; Boolean)
        {
            Caption = 'API Enabled';
            DataClassification = CustomerContent;
            InitValue = false;
        }

        field(4; "Last Sync DateTime"; DateTime)
        {
            Caption = 'Last Sync DateTime';
            DataClassification = SystemMetadata;
            Editable = false;
        }

        field(5; "Last Sync Status"; Text[100])
        {
            Caption = 'Last Sync Status';
            DataClassification = SystemMetadata;
            Editable = false;
        }
    }

    keys
    {
        key(PK; "Primary Key")
        {
            Clustered = true;
        }
    }
}
