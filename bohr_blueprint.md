# REPO BLUEPRINT: blueprint_sync_bohr

## 🏗 DATA MODELS (144 discovered)
- **Go.AdvancedVocationalBenefitApplication**: `[ID, DocumentApplyID, DocumentApply, AAttendanceFlag, BCreditsFlag, CCertificationOfEnrollmentFlag, AAttendanceFormat, BCreditsFormat]`
- **Go.ApplyCategory**: `[ID, Name, ShortName, Sort, Flag, ApplyTypes]`
- **Go.ApplyGroup**: `[ID, Name, ShortName, Sort, Flag, ApplyTypes]`
- **Go.ApplyStatus**: `[ID, Name, ShortName, Sort, Flag]`
- **Go.ApplyType**: `[ID, GroupID, Group, Name, TemplateFile, FileNameFormat, ApplicationCondition, AutomationLevel]`
- **Go.AttendClass**: `[ID, CustomerID, ScheduleID, M2MID, Date, BranchID, ClassroomID, FreeroomID]`
- **Go.AttendFlag**: `[ID, Name, ShortName, Sort, Flag]`
- **Go.Base**: `[ID, ConsumptionTax, EntrancePayPrice, BohrBaseURL]`
- **Go.BenefitContact**: `[ID, ContractID, Contract, StaffID, StateID, State, Note, Time]`
- **Go.BenefitContactState**: `[ID, Name, ShortName, Sort, Flag]`
- **Go.BenefitTarget**: `[ID, CourseID, Course, CoursePrice, CourseNum, CourseTerm, Sort, Flag]`
- **Go.BenefitType**: `[ID, Name, ShortName, Flag, Sort]`
- **Go.Branch**: `[ID, Name, Sort, Flag, OfflineFlag]`
- **Go.BusinessCategory**: `[ID, Name, ShortName, Flag, Sort]`
- **Go.ChangeContract**: `[ID, ContractID, Contract, Date, Price, TaxRate, EntrancePayPrice, TuitionPayPrice]`
- **Go.Class**: `[ID, Name, ShortName, LessonNum, GroupID, PointNum, TuitionPayPrice, Sort]`
- **Go.ClassGroup**: `[ID, Name, TuitionPayPrice, PointNum, Flag]`
- **Go.ClassLesson**: `[ID, LessonClassID, Num, MaxSeats, ExtraLesson, VideoDuration, LessonMaterial, IndDigitalTextLink]`
- **Go.ClassProgress**: `[ID, CustomerID, ClassNameID, ClassOdProgress, CompletedOdProgDate, HomeworkOdProgress, Sort, Flag]`
- **Go.ClassType**: `[ID, Name, ShortName, Flag]`
- **Go.Classroom**: `[ID, Name, ShortName, BranchID, MaxNum, Sort, Flag, Branch]`
- **Go.ClassroomClass**: `[ID, ClassroomID, ClassroomClassID, LessonNum, MaxNum, Classroom, Class]`
- **Go.ClassroomOs**: `[ID, ClassroomID, OsID, MaxNum, Classroom, Os]`
- **Go.ClassroomPeriod**: `[ID, BeginHHII, EndHHII]`
- **Go.Contract**: `[ID, CustomerID, Customer, TypeID, Type, Date, FirstTime, FirstBranchID]`
- **Go.ContractCancelType**: `[ID, Name, ShortName, Sort, Flag]`
- **Go.ContractType**: `[ID, Name, ShortName, Sort, Flag]`
- **Go.CorporateAnswers**: `[ID, QuestionID, Title, IsCorrect, Question]`
- **Go.CorporateExamSettings**: `[ID, ShortName, NoOfQues, RandomQuestionOrder, RandomAnswerOrder, PassPercent, TimeLimit, RetakeTime]`
- **Go.CorporateQuestions**: `[ID, CreateTime, Title, ClassNameID, LessonNameID, RoleID, TotalTaken, TotalCorrect]`
- **Go.Course**: `[ID, Name, Flag, Classes]`
- **Go.CourseSimulationData**: `[CourseName, ClassNames, TuitionPrice, DiscountPercent, Discount, TuitionPriceAfterDiscount, EntrancePrice, TotalPriceBeforeTax]`
- **Go.CourseSimulationRequest**: `[CalcFlag, CourseID, ClassIDs, NumLessons, ConsumptionTax, NoEntranceFee]`
- **Go.CourseSimulationResponse**: `[Status, StatusCode, Message, Data]`
- **Go.CronMail**: `[ID, Subject, Message, ToAddress, FromAddress, CreatedAt, SendAt, SentAt]`
- **Go.CustomDM**: `[ID]`
- **Go.Customer**: `[ID, StudentID, StudentPW, LoginFlag, Name, Kana, Romaji, Gender]`
- **Go.CustomerPosition**: `[ID, Name, ShortName, Flag, Sort]`
- **Go.CustomerTarget**: `[ID, Name, ShortName, Flag, Sort]`
- **Go.DocumentApply**: `[ID, Date, CustomerID, Customer, ApplyTime, ApplyTypeID, ApplyType, RequestedDocument]`
- **Go.DocumentUpload**: `[ID, CustomerID, Customer, SubmissionType, OtherType, Title, DataType, CategoryType]`
- **Go.DocumentUploadFormatted**: `[ID, CustomerID, Customer, SubmissionType, OtherType, Title, DataType, CategoryType]`
- **Go.EchonetKey**: `[ID, KeyID, Secret]`
- **Go.Enquete**: `[ID, Name, ShortName, Flag]`
- **Go.EnqueteSubmission**: `[ID, CustomerID, Customer, EnqueteID, Enquete, ContractID, Contract]`
- **Go.EnvironmentSetting**: `[ID, Name, EnvType, PdfURL, Website, Website2, Website3, Default]`
- **Go.Event**: `[ID, M2MID, Date, StartTimeHHII, EndTimeHHII, BranchID, ClassroomID, Name]`
- **Go.EventAttend**: `[ID, EventID, CustomerID, StaffID, Time, AttendStatus, ProcedureID, ImpressionFilled]`
- **Go.ExamAttend**: `[ID, ExamScheduleID, CustomerID, StaffID, Time, Note, OsID, Points]`
- **Go.ExamSchedule**: `[ID, ExamID, Date, BeginTime, EndTime, BranchID, ClassroomID, Note]`
- **Go.ExamScheduleResponse**: `[ID, Name, Date, BeginTime, EndTime, Note, TotalSeats, AvailableSeats]`
- **Go.FAQCategory**: `[ID, Name, ShortName, Sort, Flag, FAQQAs]`
- **Go.FAQQA**: `[ID, FAQTypeID, CategoryID, Question, Answer, Sort, Flag, FAQType]`
- **Go.FAQType**: `[ID, Name, ShortName, Sort, Flag, FAQQAs]`
- **Go.FileUploadRequest**: `[SubmissionType, OtherType, Title, DataType, CategoryType, Deliverables, TechRequirements, Note]`
- **Go.Freeroom**: `[ID, BranchID, Name, ShortName, MaxNum, LimitFlag, Sort, Flag]`
- **Go.FreeroomOs**: `[ID, FreeroomID, OsID, MaxNum, Freeroom, Os]`
- **Go.FreeroomPeriod**: `[ID, Num, BeginHHII, EndHHII]`
- **Go.FreeroomPeriodLimit**: `[ID, FreeroomID, PeriodID, MaintenanceDates, LimitDates, Freeroom, Period]`
- **Go.FreeroomSchedule**: `[ID, FreeroomID, Day, StartID, EndID, Freeroom, Start, End]`
- **Go.FreeroomSpecialDay**: `[ID, Year, FreeroomID, Day, StartID, EndID, Freeroom, Start]`
- **Go.IA**: `[ID, DateYYYYMM, MaintenanceDates]`
- **Go.ITTestFormattedAnswer**: `[QuestionTitle, IsCorrect, Answers]`
- **Go.ITTestFormattedAnswerItem**: `[AnswerTitle, IsSubmitted, IsCorrect]`
- **Go.ITTestResultResponse**: `[ID, ClassNameName, LessonNameName, ExamTypeName, StartTime, EndTime, Score, Passed]`
- **Go.ImpressionCatchup**: `[ID, CustomerID, Customer, PlaylistID, Playlist, ClassId, Cls, ImpressPoint1]`
- **Go.ImpressionOD**: `[ID, CustomerID, Customer, LessonID, Lesson, StaffID, Staff, PlaylistID]`
- **Go.IndAnswer**: `[ID, QuizID, QuestionID, Quiz, Question, Answers]`
- **Go.IndQuizSetting**: `[ID, Type, ClassNameID, LessonNameID, RoleGroupID, RoleID, NoOfQues, RandomQuestionOrder]`
- **Go.IndustryType**: `[ID, Name, ShortName, Flag, Sort]`
- **Go.JobKeyword**: `[ID, Name, Sort]`
- **Go.JobVacancy**: `[ID, CompanyName, PersonInCharge, Title, Furigana, Email, Phone, WebsiteURL]`
- **Go.M2M**: `[ID, CustomerID, M2MSlotID, CustomTelNum, M2MTypeID, M2MClassID, M2MClassNum, OsID]`
- **Go.M2MBranch**: `[ID, Name, Sort, Flag]`
- **Go.M2MClassQuestions**: `[ID, M2MID, Class1ID, LessonNum1, Question1, Class2ID, LessonNum2, Question2]`
- **Go.M2MControl**: `[ID, Name, ShortName, Sort, Flag]`
- **Go.M2MDesign**: `[ID, Name, ShortName, Flag, Sort]`
- **Go.M2MDevelopment**: `[ID, Name, ShortName, Flag, Sort]`
- **Go.M2MEnrollmentMethods**: `[ID, Name, ShortName, Flag, Sort]`
- **Go.M2MInstructor**: `[ID, InstructorID, MeetURL, Note, Sort, Instructor, WebsiteProduction, WebsiteDesign]`
- **Go.M2MProposal**: `[ID, Name, ShortName, Flag, Sort]`
- **Go.M2MSchedule**: `[ID]`
- **Go.M2MSlot**: `[ID, InstructorID, Date, TimeID, Instructor, Time]`
- **Go.M2MState**: `[ID, Name, ShortName, Sort, Flag]`
- **Go.M2MSubCategory**: `[ID, Name, Flag]`
- **Go.M2MTime**: `[ID, Num, BeginHHII, EndHHII, Note]`
- **Go.M2MTools**: `[ID, Name, ShortName, Flag, Sort]`
- **Go.M2MType**: `[ID, Name, ShortName, Sort, Flag]`
- **Go.M2MWebsiteProduction**: `[ID, Name, ShortName, Flag, Sort]`
- **Go.Membership**: `[ID, Name, ShortName, Sort, Flag]`
- **Go.MovieType**: `[ID, Name, Flag, Sort]`
- **Go.Notification**: `[ID, Title, Body, BodyEmail, Time, SentTo, SeenBy]`
- **Go.Occupation**: `[ID, Name, ShortName, Flag, Sort]`
- **Go.OdLog**: `[ID, CustomerID, VideoID, PlaylistID, OdClassID, OdClassNum, OdVideoNum, Count]`
- **Go.Os**: `[ID, Name, ShortName, Sort, Flag]`
- **Go.PayState**: `[ID]`
- **Go.PlayList**: `[ID, Title, InstructorID, LessonNameID, GroupNameID, Sort, TypeID, IsActive]`
- **Go.PlaylistProgress**: `[ID, CustomerID, PlaylistID, PlaylistOdProgress, Sort, Flag, Customer, Playlist]`
- **Go.PlaylistType**: `[ID, Name, ShortName, Sort, Flag]`
- **Go.Prefecture**: `[ID, Name, Code]`
- **Go.PreviousJobTitle**: `[ID, Name, ShortName, Flag, Sort]`
- **Go.PricePeriod**: `[ID, Name, Notes, Sort]`
- **Go.Procedure**: `[ID, Name]`
- **Go.PublicWorkResponse**: `[ID, CustomerID, Title, CategoryType, Deliverables, TechRequirements, WebsiteURL, Preview]`
- **Go.PublicWorksListResponse**: `[Status, StatusCode, Message, Data, Total]`
- **Go.Purpose**: `[ID, Name, ShortName, Flag, Sort]`
- **Go.QualificationCondition**: `[ID, Name, ShortName, Sort, Flag, ApplyTypes]`
- **Go.QuestionAnswer**: `[QuestionID, Title, Answers]`
- **Go.QuestionAnswerChoice**: `[AnswerID, Title]`
- **Go.QuizAnswerSubmission**: `[QuestionID, AnsOrder, Value]`
- **Go.QuizSubmissionRequest**: `[TestID, Answers]`
- **Go.QuizTaken**: `[ID, CustomerID, Start, End, ClassNameID, LessonNameID, RoleID, ExamType]`
- **Go.RecruitmentConsideration**: `[ID, Name, ShortName, Flag, Sort]`
- **Go.ReskillingCompany**: `[ID, Name, ShortName, Sort, Flag]`
- **Go.RoadmapTasks**: `[ID, ContractID, Contract, CustomerID, Customer, ClassID, Class, LessonNum]`
- **Go.RoleSubmissionGroup**: `[ID, Name]`
- **Go.ScheduleClass**: `[ID, Date, ClassroomID, ClassroomPeriodID, LessonID, StaffID, URL, Classroom]`
- **Go.Skill**: `[ID, CustomerID, TypeID, Time, QuestionNum, RightMinNum, RightNum, Result]`
- **Go.SkillAnswers**: `[ID, QuestionID, Num, Name, RightFlag, Flag, Question]`
- **Go.SkillQuestions**: `[ID, SkillTypeID, Num, Name, Flag, SkillType, Answers]`
- **Go.SkillSubmission**: `[ID, CustomerID, SkillTypeID, SkillQuestionID, SelectedAnswerID, IsCorrect, Customer, SkillType]`
- **Go.SkillType**: `[ID, Name, ShortName, QuestionNum, RightMinNum, Sort, Flag, Questions]`
- **Go.Staff**: `[ID, Name, UserID, Pic, User]`
- **Go.State**: `[ID, Name, ShortName, Sort, Flag]`
- **Go.Story**: `[ID, Name, Title, Photo, Highlight1, Highlight2, Highlight3, StudentID]`
- **Go.StoryAnswer**: `[ID, QuestionID, Question, Answer, StoryID, Story]`
- **Go.StoryCourse**: `[ID, Name, Sort, Flag]`
- **Go.StoryQuestion**: `[ID, Question, CategoryID, Category, Type, Sort, WordLimit, Flag]`
- **Go.StoryQuestionCategory**: `[ID, Name]`
- **Go.StoryTags**: `[ID, StoryID, Story, Tag, Sort]`
- **Go.StudentExam**: `[ID, Name]`
- **Go.StudentReviewRequest**: `[Age, SNS, Experience, Photo, Answers]`
- **Go.StudentReviewResponse**: `[Status, StatusCode, Message, Data]`
- **Go.SubmissionListResponse**: `[Status, StatusCode, Message, Data, Total]`
- **Go.SubmissionRequest**: `[SubmissionType, OtherType, Title, DataType, CategoryType, Deliverables, TechRequirements, Note]`
- **Go.SubmissionResponse**: `[Status, StatusCode, Message, Data]`
- **Go.TenureStatus**: `[ID, Name, ShortName, Flag, Sort]`
- **Go.UpdateSubmissionRequest**: `[SubmissionType, OtherType, Title, DataType, CategoryType, Deliverables, TechRequirements, Note]`
- **Go.User**: `[ID, FirstName, LastName, Email]`
- **Go.Video**: `[ID, PlaylistID, Name, URL, Section, Duration, Sort, IsExtra]`
- **Go.VideoGroup**: `[ID, Name, Text, Sort, IsActive]`
- **Go.VideoProgress**: `[ID, CustomerID, VideoID, VideoOdProgress, Watched, Count, Sort, Flag]`
- **Go.WorkSoftware**: `[ID, Name, Sort, Flag]`
- **Go.WorkType**: `[ID, Name, Sort, Flag]`

### 🛣 GO ROUTES
- **support.go**: `[SupportRoutes]`
- **itTest.go**: `[ITTestRoutes]`
- **submission.go**: `[SetupSubmissionRoutes]`
- **routes.go**: `[SetupRoutes]`
- **notification.go**: `[NotificationRoutes]`
- **user.go**: `[UserRoutes]`
- **auth.go**: `[AuthRoutes]`
- **reservation.go**: `[ReservationRoutes]`
- **od.go**: `[ODRoutes]`

## 📂 DIRECTORY STRUCTURE
```
├── GEMINI.md
├── Makefile
├── README.md
├── backend/
  ├── build.sh
  ├── config/
    ├── db.go
    ├── django.go
  ├── controllers/
    ├── auth.go
    ├── itTest.go
    ├── notificationController.go
    ├── odController.go
    ├── reservationController.go
    ├── submissionController.go
    ├── supportController.go
    ├── userController.go
  ├── go.mod
  ├── go.sum
  ├── main.go
  ├── middleware/
    ├── jwt.go
  ├── models/
    ├── core.go
    ├── customer.go
    ├── itTest.go
    ├── notification.go
    ├── od.go
    ├── reservation.go
    ├── submission.go
    ├── support.go
  ├── prodenv/
  ├── routes/
    ├── auth.go
    ├── itTest.go
    ├── notification.go
    ├── od.go
    ├── reservation.go
    ├── routes.go
    ├── submission.go
    ├── support.go
    ├── user.go
  ├── services/
    ├── django_file_client.go
    ├── email.go
    ├── prefecture.go
  ├── test/
    ├── auth_test.go
    ├── helpers.go
    ├── itTest_test.go
    ├── odController_test.go
    ├── reservationController_test.go
    ├── submissionController_test.go
    ├── supportController_test.go
    ├── user_test.go
  ├── tmp/
    ├── check_ia.go
    ├── check_ia_single.go
    ├── check_special.go
    ├── main
  ├── utils/
    ├── datetime.go
    ├── itTest.go
    ├── onDemand.go
    ├── reservation.go
    ├── stringUtils.go
    ├── user.go
├── docs/
  ├── backend/
    ├── apis/
  ├── frontend/
    ├── api.md
    ├── api_ittest.md
    ├── assets_css_tailwind_base.md
    ├── components_buttons_buttoncomponent.md
    ├── components_buttons_togglebutton.md
    ├── components_calendar_calendarcomponent.md
    ├── components_card_carditem.md
    ├── components_card_cardlistwrapper.md
    ├── components_copybutton.md
    ├── components_copybuttonexamples.md
    ├── components_filters_dropdowncomponent.md
    ├── components_informationbox.md
    ├── components_inputs_dateinputcomponent.md
    ├── components_inputs_inputwrapper.md
    ├── components_inputs_multidropdowncomponent.md
    ├── components_inputs_radiodatecomponent.md
    ├── components_inputs_smallcheckboxes.md
    ├── components_inputs_smallradios.md
    ├── components_inputs_textareacomponent.md
    ├── components_inputs_textinputcomponent.md
    ├── components_inputs_textradio.md
    ├── components_loadingspinner.md
    ├── components_materialicon.md
    ├── components_pages_ittest_ittestmobile.md
    ├── components_pages_ittest_ittestpc.md
    ├── components_pages_ittest_ittestresult.md
    ├── components_pages_login_forgotpasswordform.md
    ├── components_pages_login_loginform.md
    ├── components_popup_popupwrapper.md
    ├── components_table_tablecellitem.md
    ├── components_table_tableitemcount.md
    ├── components_table_tablewrapper.md
    ├── components_tooltipcomponent.md
    ├── composables_use_layout.md
    ├── composables_useclipboard.md
    ├── stores_course.md
    ├── stores_ui.md
    ├── types_table_component.md
    ├── utils_tablefunctions.md
    ├── views_forgotpasswordpage.md
    ├── views_frontpagetemplate.md
    ├── views_ittest.md
    ├── views_u1sloginpage.md
  ├── setup/
    ├── BACKEND_DEPLOYMENT.md
    ├── BACKEND_DEVELOPMENT.md
    ├── BACKEND_README.md
    ├── BACKEND_SSL.conf
    ├── FRONTEND_DEVELOPMENT.md
    ├── LOCAL_DEVELOPMENT.md
    ├── golang-api-development-guide.md
    ├── pre-commit-guide.md
├── frontend/
  ├── README.md
  ├── dist/
    ├── assets/
    ├── index.html
    ├── vite.svg
  ├── eslint.config.js
  ├── index.html
  ├── package.json
  ├── postcss.config.js
  ├── public/
    ├── vite.svg
  ├── src/
    ├── App.vue
    ├── actions/
    ├── api/
    ├── assets/
    ├── components/
    ├── composables/
    ├── data/
    ├── helpers/
    ├── main.ts
    ├── router/
    ├── stores/
    ├── style.css
    ├── types/
    ├── utils/
    ├── views/
    ├── vite-env.d.ts
  ├── tailwind.config.js
  ├── tsconfig.app.json
  ├── tsconfig.eslint.json
  ├── tsconfig.json
  ├── tsconfig.node.json
  ├── vite.config.ts
├── package-lock.json
├── package.json
├── scripts/
  ├── deploy_server.sh
  ├── dev-start-in-tmux.sh
  ├── format-go.sh
  ├── lint-go.sh
  ├── setup-dev.sh
  ├── test-runner.sh
```