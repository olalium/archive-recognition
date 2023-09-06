/*
  Warnings:

  - The `embedding` column on the `Face` table would be dropped and recreated. This will lead to data loss if there is data in the column.

*/
-- AlterTable
ALTER TABLE "Face" DROP COLUMN "embedding",
ADD COLUMN     "embedding" DECIMAL(65,30)[];
