
page 50115 "MX Role Center"
{
    Caption = 'MAINTAINX';
    PageType = RoleCenter;

    layout
    {
        area(RoleCenter)
        {
        }
    }

    actions
    {
        area(Sections)
        {
            group(MAINTAINX)
            {
                Caption = 'MAINTAINX';

                action(Equipment)
                {
                    Caption = 'Equipment';
                    ApplicationArea = All;
                    RunObject = page "MX Equipment List";
                    ToolTip = 'View and manage registered industrial equipment.';
                }

                action(HealthAssessments)
                {
                    Caption = 'Health Assessments';
                    ApplicationArea = All;
                    RunObject = page "MX Assessment List";
                    Image = History;
                    ToolTip = 'View predictive equipment health assessments.';
                }

                action(IntegrationSetup)
                {
                    Caption = 'Integration Setup';
                    ApplicationArea = All;
                    RunObject = page "MX Setup";
                    Image = Setup;
                    ToolTip = 'Configure the MAINTAINX API integration and synchronisation.';
                }
            }
        }
    }
}
