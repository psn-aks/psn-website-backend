from typing import Optional
import csv
from fastapi.responses import StreamingResponse
from io import StringIO, BytesIO

from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
from openpyxl import Workbook

from src.pharmacists.models import Pharmacist
from src.pharmacists.schemas import (
    PharmacistCreateSchema, PharmacistReadSchema, PharmacistUpdateSchema
)

# from src.core.security import BearerTokenClass, PWDHashing
# from src.db.redis import add_jti_to_blocklist

# pwd_hashing = PWDHashing()
# jwt_bearer_token = BearerTokenClass()


class PharmacistService:

    async def get_pharmacist_by_license_number(self,
                                               license_number: str):
        pharmacist = await Pharmacist.find_one(
            Pharmacist.pcn_license_number == license_number
        )

        if not pharmacist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pharmacist not found")
        return pharmacist

    async def get_all_pharmacists(self,
                                  technical_group: Optional[str] = None):

        if technical_group:
            pharmacists = await Pharmacist.find(
                Pharmacist.technical_group == technical_group
            ).to_list()
        else:
            pharmacists = await Pharmacist.find_all().to_list()

        return [await PharmacistReadSchema.from_mongo(p) for p in pharmacists]

    async def add_a_pharmacist(self,
                               data: PharmacistCreateSchema):
        pharmacist = Pharmacist(**data.model_dump())

        await pharmacist.insert()
        return await PharmacistReadSchema.from_mongo(pharmacist)

    async def get_a_pharmacist(self,
                               license_number: str):
        pharmacist = await self.get_pharmacist_by_license_number(
            license_number
        )
        return await PharmacistReadSchema.from_mongo(pharmacist)

    async def update_a_pharmacist(self,
                                  license_number: str,
                                  data: PharmacistUpdateSchema):
        pharmacist = await self.get_pharmacist_by_license_number(
            license_number)

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(pharmacist, key, value)

        await pharmacist.save()
        return await PharmacistReadSchema.from_mongo(pharmacist)

    async def delete_a_pharmacist(self,
                                  license_number: str):

        pharmacist = await self.get_pharmacist_by_license_number(
            license_number)
        await pharmacist.delete()

        return JSONResponse(
            content="Pharmacist deleted successfully",
            status_code=status.HTTP_200_OK
        )

    async def export_pharmacists_csv(self):
        pharmacists = await Pharmacist.find().to_list()

        output = StringIO()
        writer = csv.writer(output)

        fields = ["email", "full_name", "fellow", "school_attended",
                  "pcn_license_number", "induction_year", "date_of_birth",
                  "residential_address", "place_of_work", "technical_group",
                  "interest_groups", "gender", "created_at"]

        writer.writerow(fields)

        for a in pharmacists:
            writer.writerow(
                [a.email, a.full_name, a.fellow, a.school_attended,
                 a.pcn_license_number, a.induction_year, a.date_of_birth,
                 a.residential_address, a.place_of_work, a.technical_group,
                 a.interest_groups, a.gender, a.created_at
                 ])

        output.seek(0)
        headers = {
            "Content-Disposition": "attachment; filename=pharmacists.csv"
        }
        return StreamingResponse(
            output,
            media_type="text/csv",
            headers=headers
        )

    async def export_pharmacists_excel(self):
        pharmacists = await Pharmacist.find().to_list()

        fields = ["email", "full_name", "fellow", "school_attended",
                  "pcn_license_number", "induction_year", "date_of_birth",
                  "residential_address", "place_of_work", "technical_group",
                  "interest_groups", "gender", "created_at"]

        wb = Workbook()
        ws = wb.active
        ws.append(fields)

        for a in pharmacists:
            ws.append(
                [a.email, a.full_name, a.fellow, a.school_attended,
                 a.pcn_license_number, a.induction_year, a.date_of_birth,
                 a.residential_address, a.place_of_work, a.technical_group,
                 ", ".join(a.interest_groups or []),
                 a.gender, a.created_at
                 ]
            )

        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        headers = {
            "Content-Disposition": "attachment; filename=pharmacists.csv"
        }

        return StreamingResponse(
            buffer,
            media_type=(
                ("application/vnd.openxmlformats-officedocument."
                 "spreadsheetml.sheet")
            ),
            headers=headers
        )


pharmacist_svc = PharmacistService()
