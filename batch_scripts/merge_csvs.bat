REM name of the final output file
>users.csv (
   REM name of the first csv to use, will maintain header row
   type students.csv
   REM more +1 indicating to ignore the first row of the listed csv
   more +1 staff.csv
)