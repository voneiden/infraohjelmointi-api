# Generated by Django 4.1.3 on 2022-12-08 13:28

from django.db import migrations
import pandas as pd
from functools import partial
import numpy as np
import os


def migrateExcel(apps, schema_editor, budgetExcelPath=None, planExcelPath=None):

    Project = apps.get_model("infraohjelmointi_api", "Project")
    Person = apps.get_model("infraohjelmointi_api", "Person")

    if os.path.isfile(budgetExcelPath) and os.path.isfile(planExcelPath):

        # Reading all sheets, header starting from row 10,11
        budgetExcel = pd.concat(
            pd.read_excel(budgetExcelPath, sheet_name=None, header=[10, 11]),
            ignore_index=True,
        )
        # making sure all sheets have data in same format
        if len(budgetExcel.columns) != 31:
            raise Exception("Sheets don't follow the same pattern")
        # Dropping columns we don't need
        budgetExcel = budgetExcel.drop(
            budgetExcel.columns[[3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]],
            axis=1,
        )
        # replace E/K with Boolean in the Effects Housing column
        budgetExcel.iloc[:, 2] = budgetExcel.iloc[:, 2].map({"K": True, "E": False})

        # Filtering only project rows out of the dataframe
        budgetExcel = budgetExcel[
            budgetExcel[budgetExcel.columns[15]].notna()
            | budgetExcel[budgetExcel.columns[1]].notna()
            | budgetExcel[budgetExcel.columns[2]].notna()
            | budgetExcel[budgetExcel.columns[14]].notna()
        ]
        # Removing rows without project name
        budgetExcel = budgetExcel[budgetExcel[budgetExcel.columns[0]].notna()]

        # Replacing all NaN values in financial columns with 0.0
        budgetExcel.update(budgetExcel[budgetExcel.columns[3:14]].fillna(0.0))

        # Replace NaN and other arbitrary values with python None
        budgetExcel.iloc[:, 2] = budgetExcel.iloc[:, 2].replace({np.nan: False})
        budgetExcel = budgetExcel.replace({np.nan: None, "?": None})

        # Commented out script for data shift according to year
        # currYear = datetime.date.today().year
        # financeShift = list(budget_23.columns.get_level_values(0))[4] - currYear - 1
        # if financeShift != 0:
        #     finance_df = budget_23.iloc[:, 4:14]
        #     budget_23.iloc[:, 4:14] = finance_df.shift(financeShift, axis=1)

        # Filter out projects with PW Ids
        budgetExcel_Ids = budgetExcel[
            budgetExcel[budgetExcel.columns[15]].apply(type) == int
        ]

        # Filter out projects with no Ids
        budgetExcel_no_Ids = budgetExcel[
            budgetExcel[budgetExcel.columns[15]].apply(type) != int
        ]

        # Read plan excel file, column header set to row 0,1
        planExcel = pd.concat(
            pd.read_excel(planExcelPath, sheet_name=None, header=[0, 1]),
            ignore_index=True,
        )
        # making sure all sheets have data in same format
        if len(planExcel.columns) != 28:
            raise Exception("Sheets don't follow the same pattern")
        # Dropping columns we don't need
        planExcel = planExcel.drop(
            planExcel.columns[
                [
                    5,
                    6,
                    8,
                    9,
                    10,
                    11,
                    12,
                    13,
                    14,
                    15,
                    16,
                    17,
                    18,
                    19,
                    20,
                    21,
                    22,
                    23,
                    24,
                    25,
                ]
            ],
            axis=1,
        )

        # Replacing all \ " \ with related network and project Ids in sapProject column
        planExcel.iloc[:, 1] = (
            planExcel.iloc[:, 1]
            .dropna()
            .replace(['"'], method="ffill")
            .reindex(planExcel.iloc[:, 1].index)
        )
        # Replacing all \ " \ with related network and project Ids in sapNetwork column
        planExcel.iloc[:, 2] = (
            planExcel.iloc[:, 2]
            .dropna()
            .replace(['"'], method="ffill")
            .reindex(planExcel.iloc[:, 2].index)
        )

        # Filtering only project rows out of the dataframe
        planExcel = planExcel[
            planExcel[planExcel.columns[1]].notna()
            | planExcel[planExcel.columns[2]].notna()
            | planExcel[planExcel.columns[3]].notna()
            | planExcel[planExcel.columns[4]].notna()
            | planExcel[planExcel.columns[7]].notna()
        ]
        # Removing rows without project name
        planExcel = planExcel[planExcel[planExcel.columns[0]].notna()]
        # Strip spaces and capitalize
        planExcel.iloc[:, 3] = planExcel.iloc[:, 3].str.strip().str.capitalize()
        planExcel.iloc[:, 4] = planExcel.iloc[:, 4].str.strip().str.capitalize()
        # Replace NaN and other arbitrary values with python None
        planExcel = planExcel.replace({np.nan: None, "?": None})

        # Commented line to aggregate same projects existing twice with just different sapProject ids
        # for MVP this is not applicable
        # plan_23.groupby(plan_23.columns[7]).aggregate({plan_23.columns[1]: lambda x: list(x)})

        # merging Budget projects with PW ids available with Plan projects
        merged_Plan_Budget = pd.merge(
            budgetExcel_Ids,
            planExcel,
            left_on=[budgetExcel_Ids.columns[15]],
            right_on=[planExcel.columns[7]],
            how="inner",
        )
        # Fixing data discrepancy between similar columns
        merged_Plan_Budget.iloc[:, 4] = merged_Plan_Budget.iloc[:, 21]
        merged_Plan_Budget.iloc[:, 0] = merged_Plan_Budget.iloc[:, 16]
        merged_Plan_Budget.iloc[:, 14] = merged_Plan_Budget.iloc[:, 22]
        # Dropping duplicated columns
        merged_Plan_Budget = merged_Plan_Budget.drop(
            merged_Plan_Budget.columns[[22, 21, 16]],
            axis=1,
        )
        # Getting projects which exist in budget data but not in plan data
        notMerged_Budget = budgetExcel_Ids[
            ~budgetExcel_Ids[budgetExcel_Ids.columns[15]].isin(
                planExcel[planExcel.columns[7]]
            )
        ]
        # Merging the data filtered above with the data which was not used during merger
        notMerged_Budget = pd.concat([notMerged_Budget, budgetExcel_no_Ids])

        # Getting projects which exist in plan data but not in budget data
        notMerged_Plan = planExcel[
            ~planExcel[planExcel.columns[7]].isin(
                budgetExcel_Ids[budgetExcel_Ids.columns[15]]
            )
        ]
        # Transforming data from dataframes to python lists
        notMerged_Budget_data = [
            project + ("To be filled",)
            for project in zip(
                notMerged_Budget.iloc[:, 0],
                notMerged_Budget.iloc[:, 1],
                notMerged_Budget.iloc[:, 2],
                notMerged_Budget.iloc[:, 3],
                notMerged_Budget.iloc[:, 4],
                notMerged_Budget.iloc[:, 5],
                notMerged_Budget.iloc[:, 6],
                notMerged_Budget.iloc[:, 7],
                notMerged_Budget.iloc[:, 8],
                notMerged_Budget.iloc[:, 9],
                notMerged_Budget.iloc[:, 10],
                notMerged_Budget.iloc[:, 11],
                notMerged_Budget.iloc[:, 12],
                notMerged_Budget.iloc[:, 13],
                notMerged_Budget.iloc[:, 14],
                notMerged_Budget.iloc[:, 15],
            )
        ]
        notMerged_Plan_data = [
            project + ("To be filled",)
            for project in zip(
                notMerged_Plan.iloc[:, 0],
                notMerged_Plan.iloc[:, 1],
                notMerged_Plan.iloc[:, 2],
                notMerged_Plan.iloc[:, 3],
                notMerged_Plan.iloc[:, 4],
                notMerged_Plan.iloc[:, 5],
                notMerged_Plan.iloc[:, 6],
                notMerged_Plan.iloc[:, 7],
            )
        ]
        merged_Plan_Budget_data = [
            project + ("To be filled",)
            for project in zip(
                merged_Plan_Budget.iloc[:, 0],
                merged_Plan_Budget.iloc[:, 1],
                merged_Plan_Budget.iloc[:, 2],
                merged_Plan_Budget.iloc[:, 3],
                merged_Plan_Budget.iloc[:, 4],
                merged_Plan_Budget.iloc[:, 5],
                merged_Plan_Budget.iloc[:, 6],
                merged_Plan_Budget.iloc[:, 7],
                merged_Plan_Budget.iloc[:, 8],
                merged_Plan_Budget.iloc[:, 9],
                merged_Plan_Budget.iloc[:, 10],
                merged_Plan_Budget.iloc[:, 11],
                merged_Plan_Budget.iloc[:, 12],
                merged_Plan_Budget.iloc[:, 13],
                merged_Plan_Budget.iloc[:, 14],
                merged_Plan_Budget.iloc[:, 15],
                merged_Plan_Budget.iloc[:, 16],
                merged_Plan_Budget.iloc[:, 17],
                merged_Plan_Budget.iloc[:, 18],
                merged_Plan_Budget.iloc[:, 19],
            )
        ]
        johnDoe = Person.objects.create(
            firstName="John",
            lastName="Doe",
            email="johndoe@random.com",
            title="Placeholder",
            phone="041041041",
        )
        for (
            name,
            category,
            effectHousing,
            costForecast,
            bpCPlus1,
            bpCPlus2,
            pcyPlus3,
            pcyPlus4,
            pcyPlus5,
            pcyPlus6,
            pcyPlus7,
            pcyPlus8,
            pcyPlus9,
            pcyPlus10,
            note_content,
            hkrId,
            description,
        ) in notMerged_Budget_data:
            project = Project.objects.create(
                name=name,
                category=category,
                effectHousing=effectHousing,
                costForecast=costForecast,
                budgetProposalCurrentYearPlus1=bpCPlus1,
                budgetProposalCurrentYearPlus2=bpCPlus2,
                preliminaryCurrentYearPlus3=pcyPlus3,
                preliminaryCurrentYearPlus4=pcyPlus4,
                preliminaryCurrentYearPlus5=pcyPlus5,
                preliminaryCurrentYearPlus6=pcyPlus6,
                preliminaryCurrentYearPlus7=pcyPlus7,
                preliminaryCurrentYearPlus8=pcyPlus8,
                preliminaryCurrentYearPlus9=pcyPlus9,
                preliminaryCurrentYearPlus10=pcyPlus10,
                hkrId=hkrId,
                description=description,
            )
            if note_content:
                project.note_set.create(content=note_content, updatedBy=johnDoe)
        for (
            name,
            sapProject,
            sapNetwork,
            personConstruction,
            personPlanning,
            costForecast,
            note_content,
            hkrId,
            description,
        ) in notMerged_Plan_data:
            personCon = None
            personPlan = None

            if personConstruction:
                personCon, _ = Person.objects.get_or_create(
                    firstName=personConstruction,
                    lastName="blank",
                    title="Area Manager",
                    phone="000000",
                    email="blank@blank.com",
                )

            if personPlanning:
                personPlan, _ = Person.objects.get_or_create(
                    firstName=personPlanning,
                    lastName="blank",
                    title="Area Manager",
                    phone="000000",
                    email="blank@blank.com",
                )

            project = Project.objects.create(
                name=name,
                sapProject=sapProject,
                sapNetwork=sapNetwork,
                personConstruction=personCon,
                personPlanning=personPlan,
                costForecast=costForecast,
                hkrId=hkrId,
                description=description,
            )

            if note_content:
                if personPlanning:
                    project.note_set.create(
                        content=note_content,
                        updatedBy=personPlan,
                    )
                elif personConstruction:
                    project.note_set.create(
                        content=note_content,
                        updatedBy=personCon,
                    )
                else:
                    project.note_set.create(
                        content=note_content,
                        updatedBy=johnDoe,
                    )
        for (
            name,
            category,
            effectHousing,
            costForecast,
            bpCPlus1,
            bpCPlus2,
            pcyPlus3,
            pcyPlus4,
            pcyPlus5,
            pcyPlus6,
            pcyPlus7,
            pcyPlus8,
            pcyPlus9,
            pcyPlus10,
            note_content,
            hkrId,
            sapProject,
            sapNetwork,
            personConstruction,
            personPlanning,
            description,
        ) in merged_Plan_Budget_data:
            personCon = None
            personPlan = None

            if personConstruction:
                personCon, _ = Person.objects.get_or_create(
                    firstName=personConstruction,
                    lastName="blank",
                    title="Area Manager",
                    phone="000000",
                    email="blank@blank.com",
                )

            if personPlanning:
                personPlan, _ = Person.objects.get_or_create(
                    firstName=personPlanning,
                    lastName="blank",
                    title="Area Manager",
                    phone="000000",
                    email="blank@blank.com",
                )
            project = Project.objects.create(
                name=name,
                category=category,
                effectHousing=effectHousing,
                costForecast=costForecast,
                personPlanning=personPlan,
                personConstruction=personCon,
                budgetProposalCurrentYearPlus1=bpCPlus1,
                budgetProposalCurrentYearPlus2=bpCPlus2,
                preliminaryCurrentYearPlus3=pcyPlus3,
                preliminaryCurrentYearPlus4=pcyPlus4,
                preliminaryCurrentYearPlus5=pcyPlus5,
                preliminaryCurrentYearPlus6=pcyPlus6,
                preliminaryCurrentYearPlus7=pcyPlus7,
                preliminaryCurrentYearPlus8=pcyPlus8,
                preliminaryCurrentYearPlus9=pcyPlus9,
                preliminaryCurrentYearPlus10=pcyPlus10,
                hkrId=hkrId,
                description=description,
            )

            if note_content:
                if personPlanning:
                    project.note_set.create(
                        content=note_content,
                        updatedBy=personPlan,
                    )
                elif personConstruction:
                    project.note_set.create(
                        content=note_content,
                        updatedBy=personCon,
                    )
                else:
                    project.note_set.create(
                        content=note_content,
                        updatedBy=johnDoe,
                    )

    else:

        raise Exception("Wrong path for excel files")


class Migration(migrations.Migration):

    dependencies = [
        (
            "infraohjelmointi_api",
            "0006_project_category_project_effecthousing_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(
            partial(
                migrateExcel,
                budgetExcelPath="/app/infraohjelmointi_api/mock_data/budget23.xlsx",
                planExcelPath="/app/infraohjelmointi_api/mock_data/plan23.xlsx",
            )
        ),
    ]
