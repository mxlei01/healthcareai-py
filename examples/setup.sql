CREATE DATABASE SAM
GO
USE SAM
GO
CREATE SCHEMA dbo
GO
CREATE TABLE [SAM].[dbo].[HCAIPredictionClassificationBASE] (
  [BindingID] [int] ,
  [BindingNM] [varchar] (255),
  [LastLoadDTS] [datetime2] (7),
  [PatientEncounterID] [decimal] (38, 0), --< change to your grain col
  [PredictedProbNBR] [decimal] (38, 2),
  [Factor1TXT] [varchar] (255),
  [Factor2TXT] [varchar] (255),
  [Factor3TXT] [varchar] (255))
GO
CREATE TABLE [SAM].[dbo].[HCAIPredictionRegressionBASE] (
  [BindingID] [int],
  [BindingNM] [varchar] (255),
  [LastLoadDTS] [datetime2] (7),
  [PatientEncounterID] [decimal] (38, 0), --< change to your grain col
  [PredictedValueNBR] [decimal] (38, 2),
  [Factor1TXT] [varchar] (255),
  [Factor2TXT] [varchar] (255),
  [Factor3TXT] [varchar] (255))
GO