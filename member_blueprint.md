# REPO BLUEPRINT: member

## 🏗 DATA MODELS (447 discovered)
- **analytics.ConsiderationPhase**: `[name, short_name, sort, flag]`
- **analytics.ContactAccounts**: `[corporation, name, kana, email, phone1, phone2, department, department_category]`
- **analytics.CounselingSalesBar**: `[sales]`
- **analytics.DepartmentCategory**: `[name, short_name, sort, flag, objects, active_objects]`
- **analytics.FinanceImage**: `[image, report]`
- **analytics.GAClient**: `[ga_id]`
- **analytics.GAContent**: `[name, short_name, sort, flag]`
- **analytics.GAData**: `[date, client, source, medium, keyword, page_url, landing_page_url]`
- **analytics.GAKeyword**: `[short_name, sort, flag]`
- **analytics.GALandingPageURL**: `[url, sort, flag]`
- **analytics.GAMedium**: `[name, short_name, sort, flag]`
- **analytics.GAPageURL**: `[url, sort, flag]`
- **analytics.GASales**: `[ga_data, actual_sales]`
- **analytics.GASource**: `[name, short_name, sort, flag]`
- **analytics.NegoTrainingTheme**: `[name, short_name, sort, flag]`
- **analytics.NegoTrainingType**: `[name, short_name, sort, flag]`
- **analytics.Negotiations**: `[corporation, title, contact_accounts, sales_staff, sa_staff, expected_amount, conversion_probability, phase]`
- **analytics.Phase1Enquiry**: `[negotiation, title, phase_start_date, phase_end_date, enquiry_date, material_request_date, content, memo]`
- **analytics.Phase1FollowUp**: `[phase1, inquiry_date, inquiry_type, material_request_date, content, consideration_phase]`
- **analytics.Phase2Appointment**: `[negotiation, title, phase_start_date, phase_end_date, appointment_acquisition_date, appointment_date, memo, business_negotiation_type]`
- **analytics.Phase3FollowUp**: `[phase3, date, memo]`
- **analytics.Phase3Negotiation**: `[negotiation, title, phase_start_date, phase_end_date, business_talk_date, type, nego_type, client_side_participants]`
- **analytics.Phase4Proposal**: `[negotiation, title, phase_start_date, phase_end_date, training_requirements, memo, proposal_date, expected_order_date]`
- **analytics.Phase5Actions**: `[phase5, date, action_type, details]`
- **analytics.Phase5FollowUp**: `[negotiation, title, phase_start_date, phase_end_date, next_action_date, next_action_contents, additional_requirement, training_requirements]`
- **analytics.Phase6ContractAgreement**: `[negotiation, prospect_percentage, title, phase_start_date, phase_end_date, contract_date, training_requirements, contract_amount]`
- **analytics.Phase6ContractLost**: `[negotiation, title, compete_category, competitor, key_points, memo]`
- **analytics.Phase7PaperWork**: `[negotiation, title, phase_start_date, phase_end_date, memo]`
- **analytics.PositionCategory**: `[name, short_name, sort, flag, objects, active_objects]`
- **analytics.ProjectFinance**: `[project, implementatin_details, increased_sales, increased_cost]`
- **analytics.ProjectMiddleReport**: `[project, details, verify_start, verify_end, inspection_deadline, result]`
- **analytics.ProjectProfile**: `[name, incharge, verify_start, verify_end, inspection_deadline, details, expected_sales, expected_cost]`
- **analytics.ProjectProfileImage**: `[image, report]`
- **analytics.ProjectUpdateHistory**: `[staff, project, time, changes]`
- **analytics.Reminders**: `[negotiation, title, content, reminder_date, staff, email_flag, ibjbbs_flag, done_flag]`
- **analytics.ReportImage**: `[image, report]`
- **analytics.WebPage**: `[create_staff, title, url, update_staff, create_date, update_date]`
- **chat.ChatUser**: `[user, pic, name, type, created_at, objects, unread_messages]`
- **chat.ChatUserManager**: `[chat_user, chat_user]`
- **chat.Message**: `[room, chat_user, message, created_at, created_at]`
- **chat.Participant**: `[room, chat_user, unread_messages, created_at]`
- **chat.Room**: `[name, pic, last_message, platform, private, participant_count, created_at, objects]`
- **chat.RoomManager**: `[room, room, room]`
- **contact.CorpNotification**: `[creation_date, time, updated_on, removal_date, type, title, body, bohr_top_display]`
- **contact.CorpNotificationType**: `[name, short_name, sort, flag]`
- **contact.Email**: `[title, body, time, type, sent_to, seen_by, total]`
- **contact.EmailType**: `[name, short_name, sort, flag]`
- **contact.Notice**: `[type, date, title, body, ext_url, push_notification_sent, is_active, history]`
- **contact.NoticeType**: `[name, short_name, sort, flag, active_objects, objects]`
- **contact.Notification**: `[creation_date, time, removal_date, updated_on, type, destination, title, body]`
- **contact.NotificationHistory**: `[start_datetime, end_datetime, staff, notification, search_info, error_info]`
- **contact.NotificationType**: `[name, short_name, sort, flag]`
- **contest.Contest**: `[title, is_active, description, requirements_file, settings, vote_list, start_time, submission_end_time]`
- **contest.Product**: `[user, title, description, picture, file, counter, tags, contest]`
- **contest.Tag**: `[title]`
- **contract.BenefitContact**: `[contract, staff, state, note, time]`
- **contract.BenefitContactState**: `[name, short_name, sort, flag, objects, active_objects]`
- **contract.BenefitTarget**: `[course, course_price, course_num, course_term, sort, flag, objects, active_objects]`
- **contract.ChangeContract**: `[contract, date, price, tax_rate, entrance_pay_price, tuition_pay_price, reduce_reason, benefit_entrance_pay_price]`
- **contract.Contract**: `[customer, type, date, first_time, orientation_date, orientation_mail_sent, first_branch, orientation_date]`
- **contract.ContractCancelType**: `[name, short_name, sort, flag, objects, active_objects]`
- **contract.ContractType**: `[name, short_name, sort, flag, objects, active_objects]`
- **contract.PricePeriod**: `[name, notes, sort]`
- **contract.ReskillingCompany**: `[name, short_name, sort, flag, objects, active_objects]`
- **core.AccessLog**: `[user, sub_category, time, flag]`
- **core.Base**: `[consumption_tax, entrance_pay_price, bohr_base_url]`
- **core.BulletinBoardMessage**: `[date, sender, receiver, message, time_limit]`
- **core.CalendarHolidays**: `[year, dates]`
- **core.Category**: `[name, nav, sort, flag, objects, active_objects]`
- **core.CronMail**: `[cron_type, instruction, subject, body]`
- **core.DjangoErrorLog**: `[title, error_message, time, sent_flag]`
- **core.HolidayDates**: `[date]`
- **core.IA**: `[date_yyyymm, goal_price, sum_cost, maintenance_list, holiday_list, day_num, target_branch_num, target_online_num]`
- **core.Ipaddress**: `[ip_address, flag]`
- **core.Mail**: `[material_address, lesson_address, material_title, material_body]`
- **core.Nav**: `[name, short_name, link, sort, flag, objects, active_objects]`
- **core.SubCategory**: `[category, name, link, allow_user, allow_group, sort, flag, objects]`
- **corporate.AssesmentSubmision**: `[assesment_class, training, instructor, publish_flag, submit_time]`
- **corporate.Assignment**: `[training, title, deadline, notes]`
- **corporate.AssignmentSubmission**: `[assignment, corp_account, file, time]`
- **corporate.Attendance**: `[status_old, status, training, corp_account, training_schedule, update_time, fill_time, last_login]`
- **corporate.AttendanceStatus**: `[name, short_name]`
- **corporate.BlackList**: `[name, email, flag, objects, active_objects]`
- **corporate.CompeteCategory**: `[name, short_name, sort, flag, objects, active_objects]`
- **corporate.Competitor**: `[name, short_name, compete_cat, sort, flag, objects, active_objects]`
- **corporate.ContractLostReason**: `[name, short_name, sort, flag, objects, active_objects]`
- **corporate.CorpAccounts**: `[corporation, user, is_admin, password, name, kana, email, email_verified]`
- **corporate.CorpAdminNotification**: `[training, top_page_display, creation_date, display_datetime, type, title, body, seen_by]`
- **corporate.CorpBenefit**: `[name, version_start, version_end, objects]`
- **corporate.CorpBenefitApplicationCondition**: `[benefit, document_name, document_number, empty_doc, example_doc, condition, objects]`
- **corporate.CorpBenefitApplicationGeneral**: `[benefit, document_name, document_number, empty_doc, example_doc, objects]`
- **corporate.CorpBenefitChangeCondition**: `[benefit, document_name, document_number, empty_doc, example_doc, condition, objects]`
- **corporate.CorpBenefitChangeGeneral**: `[benefit, document_name, document_number, empty_doc, example_doc, objects]`
- **corporate.CorpBenefitConditions**: `[name, short_name, sort, flag, objects, active_objects]`
- **corporate.CorpBenefitName**: `[name, short_name, sort, flag, objects, active_objects]`
- **corporate.CorpBenefitPlanningCondition**: `[benefit, document_name, document_number, empty_doc, example_doc, condition, objects]`
- **corporate.CorpBenefitPlanningGeneral**: `[benefit, document_name, document_number, empty_doc, example_doc, objects]`
- **corporate.CorpBenefitSubmission**: `[training, planning_general, change_general, application_general, planning_condition, change_condition, application_condition, creation_time]`
- **corporate.CorpCall**: `[corporation, staff, negotiation, phase, note, time, mail_body, mail_from]`
- **corporate.CorpClassProgress**: `[corp_account, class_name, progress, completed_progress_time, flag, active_objects, objects]`
- **corporate.CorpClasses**: `[name, short_name, lesson_num, sort, flag, objects, active_objects]`
- **corporate.CorpDocuments**: `[title, training, corp_account, creation_date, file, status]`
- **corporate.CorpEnquete**: `[name, training, flag, edit, deadline, edit_time, create_time, time_to_take]`
- **corporate.CorpEnqueteAnswer**: `[title, question]`
- **corporate.CorpEnqueteQuestion**: `[title, enquete, type, required]`
- **corporate.CorpEnqueteSubmission**: `[corp_account, training, enquete, latest_submission, answer_submission]`
- **corporate.CorpEnqueteType**: `[name, short_name]`
- **corporate.CorpImpression**: `[corp_account, training, training_schedule, name, impress_point1, impress_point2, impress_point3, impress_note]`
- **corporate.CorpImpressionOD**: `[corp_account, training, lesson, playlist, video, impress_point1, impress_point2, impress_point3]`
- **corporate.CorpIndustryType**: `[name, short_name, point, parent, flag, sort]`
- **corporate.CorpIndustryTypeCat**: `[name, short_name, flag, sort]`
- **corporate.CorpListing**: `[name, short_name, point, flag, sort]`
- **corporate.CorpODCompleted**: `[training, corp_account, lesson_list, date_dict, date_dict, date_dict]`
- **corporate.CorpPlaylistProgress**: `[corp_account, playlist, progress, flag, active_objects, objects]`
- **corporate.CorpStaffType**: `[name, short_name, sort, flag]`
- **corporate.CorpState**: `[name, short_name, sort, flag, objects, active_objects]`
- **corporate.CorpSubsidyType**: `[name, short_name, flag, sort]`
- **corporate.CorpVideoProgress**: `[corp_account, video, video_num, class_name, lesson_num, progress, watched, count]`
- **corporate.CorpVideosWatchHistory**: `[corp_video_progress, date_id, session_open_time, session_close_time]`
- **corporate.CorporateAnswers**: `[question, title, is_correct, text, text, text]`
- **corporate.CorporateCommonSettings**: `[classes_note, note_admin]`
- **corporate.CorporateExamSettings**: `[short_name, no_of_ques, random_question_order, random_answer_order, pass_percent, time_limit, retake_time]`
- **corporate.CorporateQuestions**: `[create_time, title, class_name, lesson_name, role, total_taken, total_correct, mini_exam_flag]`
- **corporate.CorporateSubmission**: `[corp_account, class_name, lesson_name, exam_type, training, start_time, end_time, score]`
- **corporate.CorporateUpdateHistory**: `[staff, corporation, training, time, page_updated, changes]`
- **corporate.Corporation**: `[name, first_name, url, kana, gender, birth_yyyymmdd, state, staff]`
- **corporate.CorporationCron**: `[name, staff, time]`
- **corporate.CustomizedSkill**: `[training, skill, sort]`
- **corporate.DailyReportMessage**: `[training, corp_account, reply_to, creation_date, body, title, training_date, student]`
- **corporate.EmailToCorp**: `[title, body, time, email_from, sent_to, cc_to, bcc_to, seen_by]`
- **corporate.EmployeesNumberRange**: `[name, short_name, point, flag, sort]`
- **corporate.EnvironmentManualSetting**: `[training, name, software_name, url, remarks, flag, note_student]`
- **corporate.EnvironmentSetting**: `[name, env_type, pdf_url, website, website2, website3, default, sort]`
- **corporate.InstructorStudentAssesment**: `[corp_account, training, point1, point2, assesment_class, instructor, note, time]`
- **corporate.InterviewState**: `[name, short_name, sort, flag, objects, active_objects]`
- **corporate.ItSkill**: `[name, short_name, sort, flag, objects, active_objects]`
- **corporate.LastVideoInfo**: `[training, corp_account, date, video]`
- **corporate.MaxNumberStudents**: `[name, short_name, point, sort, flag, objects, active_objects]`
- **corporate.ODReminderEmail**: `[training, type, frequency, body, flag, objects, active_objects]`
- **corporate.QAReport**: `[parent, corp_account, training, lesson, title, content, time]`
- **corporate.Reaction**: `[user, report, emoji]`
- **corporate.Report**: `[parent, corp_account, training, title, content, time, seen_by, data]`
- **corporate.ServiceMode**: `[name, short_name, flag, sort]`
- **corporate.SkillConfig**: `[training, skill_check_flag, customized_flag, comment_flag, skill_low_flag, skill_avg_flag, show_ranking, random_question_order]`
- **corporate.StudentClassAssesment**: `[corp_account, training, point1, point2, assesment_class, note, time, published]`
- **corporate.TextbookManual**: `[training, name, software_name, url, remarks, flag, note_student]`
- **corporate.TraineeComment**: `[corp_account, training, comment, staff]`
- **corporate.TraineeCustomizedSkill**: `[corp_account, customized_skill, score]`
- **corporate.Training**: `[corporation, category, skill_level, instruction_skill, corp_accounts, mode, title, type]`
- **corporate.TrainingBill**: `[training, contract_date, tuition_pay_price, tax_rate, sale_tax, amount_of_payment, contract_type, negotiation_title]`
- **corporate.TrainingCategory**: `[name]`
- **corporate.TrainingDefaultReminder**: `[title, note, sort, flag, objects, active_objects]`
- **corporate.TrainingMode**: `[name, short_name, sort, flag, objects, active_objects]`
- **corporate.TrainingNote**: `[name, content]`
- **corporate.TrainingNotice**: `[training, notice, created_at, updated_at]`
- **corporate.TrainingReminder**: `[training, deadline, title, remind_staff, note, finished, created_at, created_by_staff]`
- **corporate.TrainingReport**: `[training, name, file, updated_by, updated_at, created_at, display]`
- **corporate.TrainingSchedule**: `[training, date, start_time, end_time, title, url, zoom_password, location]`
- **corporate.TrainingTextbook**: `[class_name, url, note_student, note, flag, sort]`
- **corporate.TrainingType**: `[name, short_name, sort, flag, objects, active_objects]`
- **customer.BenefitType**: `[name, short_name, flag, sort, apply_type]`
- **customer.BusinessCategory**: `[name, short_name, flag, sort]`
- **customer.CallState**: `[name, short_name, sort, flag, objects, active_objects]`
- **customer.CancelType**: `[name, short_name, sort, flag]`
- **customer.Cancellation**: `[customer, time_created, time_udpated, staff_last_updated, cancel_type, refund_amount, dismissal_application_date, other_discount_amount]`
- **customer.CancellationReason**: `[name, short_name, sort, flag]`
- **customer.CounsellingData**: `[customer, time_created, q1, q2, q3, q4, q5, q6]`
- **customer.CustCancelData**: `[cancel, time_updated, num1, num2, num3, num4, num5, num6]`
- **customer.CustomApply**: `[customer, staff, call_state, apply_type, note, time, mail_to, mail_from]`
- **customer.CustomCall**: `[customer, staff, call_state, note, time, mail_to, mail_from, mail_title]`
- **customer.CustomCallHistory**: `[date_time, custom_call, staff]`
- **customer.CustomDM**: `[name, num, staff, type, note, sort, flag, objects]`
- **customer.CustomDMType**: `[name, sort, flag, objects, active_objects]`
- **customer.CustomDownload**: `[file, title, image1, image2, points, upload_staff, sort, flag]`
- **customer.CustomDownloadHistory**: `[custom_download, customer, points, time]`
- **customer.CustomImport**: `[material_route, material_request_time, time, staff_id, name, kana, gender, birth_yyyymmdd]`
- **customer.CustomMembership**: `[name, short_name, sort, flag, objects, active_objects]`
- **customer.CustomState**: `[name, short_name, sort, flag, objects, active_objects]`
- **customer.CustomStatus**: `[name, short_name, sort, flag]`
- **customer.CustomTelNg**: `[customer, name, kana, phone, media, note, time, staff]`
- **customer.Customer**: `[user, name, kana, romaji, gender, contact_cautions, prefered_contact, birth_yyyymmdd]`
- **customer.CustomerPosition**: `[name, short_name, flag, sort]`
- **customer.CustomerStats**: `[customer, date, ondemand_count, ondemand_time, latest_ondemand_time, m2m_count, m2m_time, latest_m2m_time]`
- **customer.CustomerTarget**: `[name, short_name, flag, sort]`
- **customer.CustomerUpdateHistory**: `[staff, customer, time, page_updated, changes]`
- **customer.DocumentUpload**: `[customer, submission_type, other_type, title, data_type, category_type, deliverables, tech_requirements]`
- **customer.DocumentUploadMailHistory**: `[document_upload, customer, mail_to, mail_from, mail_title, mail_body, status, staff]`
- **customer.EchonetKey**: `[email, api_key, login, password, used_flag, dummy_key]`
- **customer.EchonetResultUpload**: `[date, email_sent, file, staff]`
- **customer.Enquete**: `[title, short_name, description, sort, flag, edit_time, create_time, objects]`
- **customer.EnqueteOption**: `[label, question]`
- **customer.EnqueteQuestion**: `[label, enquete, question_type, other_option, parent_question, required]`
- **customer.EnqueteQuestionType**: `[name, short_name]`
- **customer.EnqueteSubmission**: `[customer, contract, enquete, fill_time, data]`
- **customer.Gform**: `[customer, email, name, age, todofuken, address, school, job_type]`
- **customer.GformMemo**: `[customer, memo]`
- **customer.GformNew**: `[customer, fill_time, email, name, age, zipcode, address, job_type]`
- **customer.GformNewMemo**: `[customer, memo]`
- **customer.IndustryType**: `[name, short_name, flag, sort]`
- **customer.Infra**: `[name, short_name, sort, flag, objects, active_objects]`
- **customer.Media**: `[name, short_name, list_flag, sort, flag, objects, active_objects]`
- **customer.MovieType**: `[name, flag, sort]`
- **customer.Occupation**: `[name, short_name, flag, sort]`
- **customer.PreviousJobTitle**: `[name, short_name, flag, sort]`
- **customer.Purpose**: `[name, short_name, flag, sort]`
- **customer.RecuitmentConsideration**: `[name, short_name, flag, sort]`
- **customer.ReferralMatch**: `[inviter, invitee, gift_sent_flag, date_add, date]`
- **customer.ReskillEnd**: `[update_time, date_of_issue, customer, zipcode, address, name, kana, custom_start_date]`
- **customer.ReskillHalf**: `[update_time, date_of_issue, customer, zipcode, address, name, kana, custom_start_date]`
- **customer.ReskillUnemployment**: `[update_time, date_of_issue, customer, name, custom_start_date, custom_end_date, remark, same_address]`
- **customer.Role**: `[title, short_name, description, description_color, icon, skills, sort, flag]`
- **customer.RoleGroup**: `[title, short_name, description, description_background_color, button_color, sort, flag, objects]`
- **customer.RoleSubmission**: `[type, customer, role, m2m, sub_group, sort, url_link, file_upload]`
- **customer.RoleSubmissionGroup**: `[customer, role, sort, name, popup, popup_viewed, created_time, edit_time]`
- **customer.RoleSubmissionScore**: `[name, short_name, sort, score]`
- **customer.RoleSubmissionType**: `[name, short_name, weight, sort]`
- **customer.StudentSchedule**: `[customer, learner_type, custom_hours, schedule_items, schedule_row_info, scheduled_completion_date, updated_date_time, schedule_delay_alert]`
- **customer.TenureStatus**: `[name, short_name, flag, sort]`
- **customer.TopMessage**: `[title, message, sort, start_timing, percentage, condition, end_timing, display_period]`
- **data_analysis.AnalysisReport**: `[name, date, description, report_type, which_date, start_date, end_date, group_dict]`
- **equipment.Branch**: `[name, sort, flag, offline_flag, objects, active_objects]`
- **equipment.Classroom**: `[branch, name, short_name, max_num, sort, flag, objects, active_objects]`
- **equipment.ClassroomClass**: `[classroom, classroom_class, lesson_num, max_num]`
- **equipment.ClassroomOs**: `[classroom, os, max_num]`
- **equipment.ClassroomPeriod**: `[num, begin_hhii, end_hhii]`
- **equipment.Freeroom**: `[branch, name, short_name, max_num, limit_flag, sort, flag, objects]`
- **equipment.FreeroomOs**: `[freeroom, os, max_num]`
- **equipment.FreeroomPeriod**: `[num, begin_hhii, end_hhii, ia_obj, freeroom, freeroom_period_limit_obj, freeroom_period_limit_obj, special_day]`
- **equipment.FreeroomPeriodLimit**: `[freeroom, period, maintenance_dates, limit_dates, dates, date_obj, start, end]`
- **equipment.FreeroomSchedule**: `[freeroom, day, start, end]`
- **equipment.FreeroomSpecialDay**: `[year, freeroom, day, start, end]`
- **equipment.Os**: `[name, short_name, sort, flag, objects, active_objects]`
- **event.Event**: `[m2m, date, start_time_hhii, end_time_hhii, branch, classroom, name, note]`
- **event.EventAttend**: `[event, customer, staff, time, attend_status, procedure, impression_filled, date_today]`
- **event.EventImpression**: `[customer, event, impress_point1, impress_point2, impress_point3, impress_note, fill_time]`
- **exam.DXAnswer**: `[text, flag, question, weight, objects, active_objects]`
- **exam.DXCatScore**: `[subcategory, sitting, score]`
- **exam.DXCategory**: `[name, short_name, sort, flag, objects, active_objects]`
- **exam.DXQuestion**: `[title, subcategory, difficulty, flag, objects, active_objects]`
- **exam.DXQuestionDifficulty**: `[name, short_name, flag, sort]`
- **exam.DXSubCategory**: `[name, cat_name, short_name, sort, flag, score, category, objects]`
- **exam.DXTest**: `[title, corporation, expiration_date, test_url, active, admin_email, creation_date]`
- **exam.DXTestSitting**: `[corporation, register_date, test_url, corp_account, dx_test, dsa_sitting_string, dsa_score, dsa_submit_time]`
- **exam.ExamAttend**: `[exam_schedule, customer, staff, time, note, os, points, result]`
- **exam.ExamSchedule**: `[exam, date, begin_hhii, end_hhii, branch, classroom, note, max_num]`
- **exam.ExamType**: `[name, short_name, sort, flag, objects, active_objects]`
- **exam.Skill**: `[customer, type, time, question_num, right_min_num, right_num, result, answers]`
- **exam.SkillAnswers**: `[question, num, name, right_flag, flag, objects, active_objects]`
- **exam.SkillQuestions**: `[skill_type, num, name, flag, objects, active_objects]`
- **exam.SkillType**: `[name, short_name, question_num, right_min_num, sort, flag, objects, active_objects]`
- **exam.StudentExam**: `[name, short_name, exam_type, sort, flag, objects, active_objects]`
- **ia_admin.IndAnswer**: `[question, answer, quiz]`
- **ia_admin.IndQuizSetting**: `[type, class_name, lesson_name, role_group, role, no_of_ques, random_question_order, random_answer_order]`
- **ia_admin.QuizTaken**: `[customer, start, end, class_name, lesson_name, role, exam_type, setting]`
- **instructor.Certification**: `[name, name_ja, short_name, sort, flag]`
- **instructor.InstructorAccountType**: `[name, short_name, sort, flag, objects]`
- **instructor.InstructorAccounts**: `[staff, account_type, password, username]`
- **instructor.InstructorCertification**: `[staff, certification, date, status]`
- **instructor.InstructorLesson**: `[staff, date, lesson, lesson_status, supervisor]`
- **instructor.LessonStatus**: `[name, short_name, sort, flag]`
- **instructor.ProSkill**: `[type, staff, title, time]`
- **instructor.ProType**: `[name, short_name, sort, flag]`
- **job_outsourcing.JobOffer**: `[number, title, clause, level, application_deadline, deadline, production_number, salary]`
- **job_outsourcing.JobOfferApplication**: `[job_offer, applicant, flag, status, date, objects, active_objects]`
- **job_outsourcing.JobOfferHistory**: `[date, submit_staff, changes, job_offer]`
- **job_outsourcing.JobOutTag**: `[name, short_name, sort, flag, objects, active_objects]`
- **job_outsourcing.Level**: `[name, short_name, sort, flag, objects, active_objects]`
- **job_outsourcing.MembershipForm**: `[customer, sakuhin, experience, status, flag, date, objects, active_objects]`
- **job_outsourcing.MembershipHistory**: `[date, submit_staff, changes, membership]`
- **job_outsourcing.StatusMembership**: `[name, short_name, sort, flag, objects, active_objects]`
- **job_outsourcing.StatusOffer**: `[name, short_name, sort, flag, objects, active_objects]`
- **knowledge_centre.AccessGroups**: `[name, short_name, sort, flag]`
- **knowledge_centre.FAQCategory**: `[name, short_name, sort, flag, objects, active_objects]`
- **knowledge_centre.FAQQA**: `[faq_type, category, question, answer, sort, flag, objects, active_objects]`
- **knowledge_centre.FAQType**: `[name, short_name, sort, flag, objects, active_objects]`
- **knowledge_centre.ImpactRange**: `[name, short_name, sort, flag]`
- **knowledge_centre.KnowledgeCentre**: `[title, contributor, date_of_occurance, type, impact_range, detail, file, access_groups]`
- **knowledge_centre.KnowledgeType**: `[name, short_name, sort, flag]`
- **library.Book**: `[title, author, targets, category, image, location]`
- **library.BookCategory**: `[name, sort, flag]`
- **library.BookReservation**: `[staff, book, start_date, end_date, future, extended]`
- **library.BookTarget**: `[name, sort, flag]`
- **maintenance.Application**: `[name, short_name, sort, flag, person_in_charge, objects, active_objects]`
- **maintenance.Modif**: `[status, priority, application, page_or_function_en, page_or_function_jp, details_en, details_jp, reporter]`
- **maintenance.Priority**: `[name, short_name, sort, flag, objects, active_objects]`
- **maintenance.Status**: `[name, short_name, sort, flag, objects, active_objects]`
- **payment.ContractBranch**: `[name, sort, flag, objects, active_objects]`
- **payment.PayCard**: `[name, sort, flag, objects, active_objects]`
- **payment.PayCreditCompany**: `[name, sort, flag, objects, active_objects]`
- **payment.PayState**: `[name, short_name, sort, flag, objects, active_objects]`
- **payment.PayWay**: `[name, sort, type, flag, objects, active_objects]`
- **payment.Payment**: `[contract, training, date, plan_price, set_price, way, card, credit_company]`
- **payment.PaymentItem**: `[payment_slip, name, num, unit, price, is_discount]`
- **payment.PaymentSlip**: `[training, date, no, title, note, memo, date_apply, logo_type]`
- **qasystem.PracticalQA**: `[question_title, question, answer, likes, classes, tags, show, create_time]`
- **qasystem.Tags**: `[name, flag, sort]`
- **questionnaire.Answer**: `[name, sort, flag, question, checkbox_flag, text_flag, text_area_flag, text]`
- **questionnaire.Question**: `[name, sort, flag, category, requirement_flag, radio_flag, objects, active_objects]`
- **questionnaire.Questionnaire**: `[name, short_name, sort, flag, objects, active_objects]`
- **questionnaire.QuestionnaireBrowsingUser**: `[customer, questionnaire, objects, active_objects]`
- **questionnaire.QuestionnaireCategory**: `[name, short_name, sort, flag, questionnaire, objects, active_objects]`
- **questionnaire.UserAnswer**: `[customer, answer, check_box_value, text_value, date]`
- **quiz.Answer**: `[question, content, is_correct, sort]`
- **quiz.Question**: `[quiz, topics, content, explanation, type, level, answer_order, successful_submissions]`
- **quiz.Quiz**: `[trainings, topics, title, description, url, random_order, random_order_answer, max_questions]`
- **quiz.Sitting**: `[user, quiz, question_order, correct_questions, incorrect_questions, user_answers, order_answers, score]`
- **quiz.SittingManager**: `[questions, question_order]`
- **quiz.Topic**: `[topic_group, name, short_name]`
- **quiz.TopicGroup**: `[name, short_name]`
- **reservation.CustomAnalysis**: `[staff, name, explanation, selection, type]`
- **reservation.FollowUp**: `[yomi_data, next_action_date, next_action_contents, additional_requirement, expected_order_date, prospect_percentage, return_visit_date, memo]`
- **reservation.IndividualYomiData**: `[customer, feedback_staff, classes, courses, benefit_course, prospect_percentage, pre_confirmed_flag, thank_you_call_flag]`
- **reservation.Reminders**: `[yomi_data, title, content, reminder_date, staff, email_flag, ibjbbs_flag, done_flag]`
- **school.AdvancedVocationalBenefitApplication**: `[document_apply, a_attendance_flag, b_credits_flag, c_certification_of_enrollment_flag, a_attendance_format, b_credits_format, a_attendance_file, b_credits_file]`
- **school.ApplyCategory**: `[name, short_name, sort, flag, active_objects, objects]`
- **school.ApplyGroup**: `[name, short_name, sort, flag, active_objects, objects]`
- **school.ApplyStatus**: `[name, short_name, sort, flag]`
- **school.ApplyType**: `[group, categories, name, template_file, file_name_format, application_condition, qualification_conditions, automation_level]`
- **school.AttendClass**: `[customer, schedule, m2m, date, branch, classroom, freeroom, classroom_period]`
- **school.AttendFlag**: `[name, short_name, sort, flag, objects, active_objects]`
- **school.Category**: `[name, short_name, sort, flag]`
- **school.Class**: `[name, short_name, lesson_num, group, point_num, tuition_pay_price, sort, flag]`
- **school.ClassGroup**: `[name, point_num, tuition_pay_price, sort, flag, objects, active_objects]`
- **school.ClassLesson**: `[category, lesson_class, num, max_seats, extra_lesson, video_duration, lesson_material, training_environment]`
- **school.ClassProgress**: `[customer, class_name, class_od_progress, completed_od_prog_date, homework_od_progress, sort, flag, lesson_ids_watched]`
- **school.ClassType**: `[name, short_name, color, sort, flag, objects, active_objects]`
- **school.ClassVersion**: `[class_instance, version, update_cost, change_note, changed_at]`
- **school.CorporateCategory**: `[name, short_name, sort, flag]`
- **school.Course**: `[name, short_name, benefit_category, skill_category, sales_start_date, sales_end_date, classes, point_num]`
- **school.CurSheet**: `[staff, file, cur_sheet_class, cur_sheet_class_num, point, time, edit_time]`
- **school.DocumentApply**: `[date, customer, apply_time, apply_type, requested_document, benefit_type, status, reserved_date]`
- **school.ITgreeting**: `[date, type, ip, a1, a2, a3, result]`
- **school.ImpressionBase**: `[customer, playlist, impress_point1, impress_point2, impress_point3, impress_note, created_at, edited_at]`
- **school.ImpressionCatchup**: `[cls]`
- **school.ImpressionOD**: `[customer, lesson, staff, playlist, video, impress_point1, impress_point2, impress_point3]`
- **school.M2M**: `[customer, m2m_slot, custom_tel_num, m2m_type, m2m_class, m2m_class_num, os, request_staff]`
- **school.M2MBranch**: `[name, sort, flag, objects, active_objects]`
- **school.M2MCheckItems**: `[type, title, sort, flag, active_objects, objects]`
- **school.M2MCheckTypes**: `[name, short_name, sort, flag, active_objects, objects]`
- **school.M2MClassQuestions**: `[m2m, class_1, lesson_num_1, question_1, class_2, lesson_num_2, question_2, class_3]`
- **school.M2MContact**: `[m2m, type, note, staff, time]`
- **school.M2MContactType**: `[name, short_name, sort, flag, objects, active_objects]`
- **school.M2MControl**: `[name, short_name, sort, flag, objects, active_objects]`
- **school.M2MDesign**: `[name, short_name, flag, sort, objects, active_objects]`
- **school.M2MDevelopment**: `[name, short_name, flag, sort, objects, active_objects]`
- **school.M2MEmail**: `[customer, title, body, time, type, contact, is_seen, top_page]`
- **school.M2MEmailTemplate**: `[name, type, subject, body]`
- **school.M2MEnrollmentMethods**: `[name, short_name, sort, flag, objects, active_objects]`
- **school.M2MFeedback**: `[m2m, assignment, message, instructor_note, created_at]`
- **school.M2MInstructor**: `[instructor, website_production, website_design, website_development, website_proposal, course, os, meet_url]`
- **school.M2MProposal**: `[name, short_name, flag, sort, objects, active_objects]`
- **school.M2MSchedule**: `[date1, begin_hhii1, end_hhii1, date2, begin_hhii2, end_hhii2, date3, begin_hhii3]`
- **school.M2MSlot**: `[instructor, date, time, objects]`
- **school.M2MState**: `[name, short_name, sort, flag, objects, active_objects]`
- **school.M2MSubCategory**: `[name, main_category, flag, objects, active_objects]`
- **school.M2MTime**: `[num, begin_hhii, end_hhii, note]`
- **school.M2MTools**: `[name, short_name, sort, flag, objects, active_objects]`
- **school.M2MType**: `[name, short_name, sort, flag, objects, active_objects]`
- **school.M2MWebsiteProduction**: `[name, short_name, flag, sort, objects, active_objects]`
- **school.Material**: `[filename, file, material_type, staff, sort, flag, time]`
- **school.MaterialType**: `[name, short_name, sort, flag]`
- **school.NPSsurvey**: `[customer, referral_point, note, query, location, created_at, reject_flag]`
- **school.NPSsurveyLocation**: `[name, short_name, flag]`
- **school.ODAd**: `[ad_name, file_input, ad_link, date]`
- **school.OdLog**: `[customer, video, playlist, od_class, od_class_num, od_video_num, count, time]`
- **school.OndemandPopup**: `[date_s, date_e, title, content, created_staff, time, display]`
- **school.OpenClass**: `[title, iahp_category, start_date, end_date, date_text, start_time, end_time, time_text]`
- **school.OpenClassCategory**: `[name, short_name, sort, flag]`
- **school.OpenClassOrders**: `[date, corporation, buyer_account, open_classes, amount, trainings, tracking_id, transaction_id]`
- **school.Opinion**: `[customer, custom_name, category, custom_staff, report_staff, happen_time, send_time, type]`
- **school.OpinionLevel**: `[num, name, sort, flag, objects, active_objects]`
- **school.OpinionResultType**: `[name, short_name, sort, flag, objects, active_objects]`
- **school.OpinionType**: `[name, short_name, sort, flag, objects, active_objects]`
- **school.PlayList**: `[title, category, is_new, instructor, lesson_name, group_name, sort, type]`
- **school.PlaylistProgress**: `[customer, playlist, playlist_od_progress, sort, flag, active_objects, objects]`
- **school.PlaylistType**: `[name, short_name, sort, flag, active_objects, objects]`
- **school.Procedure**: `[customer, staff, point_date, procedure_name, contract, contract_point_num, cross_contract, cross_contract_point_num]`
- **school.ProcedureName**: `[name, short_name, point_num, sort, flag, objects, active_objects]`
- **school.QualificationCondition**: `[name, short_name, sort, flag, active_objects, objects]`
- **school.Reception**: `[customer, date, branch, class_staff, post_time, impress_point1, impress_note]`
- **school.Roadmap**: `[course, class_field, self_study, other_course, original_site_production, month, small_test, big_test]`
- **school.RoadmapTasks**: `[contract, customer, class_field, lesson_num, type, month, start_date, end_date]`
- **school.RoleProgress**: `[customer, role, role_progress, completed_role_date]`
- **school.RoutineFile**: `[date, routine_type, file, staff, objects, active_objects]`
- **school.RoutineType**: `[name, short_name, sort, flag, objects, active_objects]`
- **school.ScheduleClass**: `[date, classroom, classroom_period, lesson, staff, url, start_time]`
- **school.Video**: `[playlist, name, url, section, duration, sort, is_extra, flag]`
- **school.VideoGroup**: `[name, text, sort, is_active]`
- **school.VideoProgress**: `[customer, video, video_od_progress, watched, count, sort, flag, active_objects]`
- **staff.Company**: `[name, short_name, color, sort, flag, objects, active_objects]`
- **staff.ConcernedPerson**: `[staff, factor, project]`
- **staff.CorpStudentDepartmentFin**: `[date, previous_contribution, current_contribution, department]`
- **staff.Department**: `[name, short_name]`
- **staff.Director**: `[date_yyyymm, staff, free_hour]`
- **staff.DirectorWork**: `[date_yyyymm, staff, phase, name, hour]`
- **staff.ImpressStaffManager**: `[queryset]`
- **staff.IndStudentDepartmentFin**: `[date, additional_sales_p, referral_sales_p, cancellation_sales_p, additional_sales_c, referral_sales_c, cancellation_sales_c, department]`
- **staff.Instructor**: `[date_yyyymm, staff, cost]`
- **staff.JobKeyword**: `[name, sort]`
- **staff.JobVacancy**: `[company_name, person_in_charge, title, furigana, email, phone, website_url, recruitment_type]`
- **staff.PersonInCharge**: `[staff]`
- **staff.Phase**: `[name, short_name, sort, flag, objects, active_objects]`
- **staff.Position**: `[name, sort, flag, objects, active_objects]`
- **staff.ProfTime**: `[num, begin_hhii, end_hhii]`
- **staff.ProfType**: `[name, short_name, color, sort, flag, objects, active_objects]`
- **staff.Project**: `[name, department, performance, release_date, details, url]`
- **staff.ProjectPerformance**: `[difficulty, speed, quality]`
- **staff.ProspectDepartmentFin**: `[date, actual_sales, sales_on_analytics, department]`
- **staff.ProspectProjectFin**: `[date, page_views, page_value, outsourcing_expense, labor_cost, project]`
- **staff.Sales**: `[date_yyyymm, staff, cost, commit, add_point]`
- **staff.SalesPrice**: `[num, begin_price, end_price]`
- **staff.SalesScheduleMemo**: `[date, staff, memo]`
- **staff.SalesScheduleReport**: `[date, time, occupied, available]`
- **staff.SalesStaffCategory**: `[name, short_name, sort, flag]`
- **staff.SalesStaffPriority**: `[date, staff, num, sales, num_customers, online_flag]`
- **staff.SalesTime**: `[num, begin_hhii, end_hhii]`
- **staff.SalesType**: `[name, color, sort, flag, objects, active_objects]`
- **staff.SchProf**: `[staff, date, prof_time, prof_type, note, span, submit_staff, google_calendar_id]`
- **staff.SchSales**: `[staff, date, sales_time, sales_type, branch, place, note, span]`
- **staff.ScheduleHistory**: `[date, old_staff, new_staff, old_date, new_date, submit_staff, changes, old_schedule]`
- **staff.Section**: `[name, short_name, sort, flag, objects, active_objects]`
- **staff.Staff**: `[user, pic, od_icon, kana, company, section, position, sales_category]`
- **staff.StudentProjectFin**: `[date, sales_increase, costs_increase, project]`
- **stories.AnswerGraduate**: `[question, answer, answer_file, answer_image, story]`
- **stories.AnswerStudent**: `[question, answer, answer_file, answer_image, story]`
- **stories.StoriesGraduateQuestion**: `[question, category, choices, sort, flag]`
- **stories.StoriesGraduateQuestionCategory**: `[category, sort]`
- **stories.StoriesStudentQuestion**: `[question, category, choices, sort, flag]`
- **stories.StoriesStudentQuestionCategory**: `[category, sort]`
- **stories.StoryGraduate**: `[name, title, photo, tags, highlight1, highlight2, highlight3, student_id]`
- **stories.StoryStudent**: `[name, title, photo, tags, highlight1, highlight2, highlight3, student_id]`
- **story.IAHPpages**: `[app, name, file]`
- **story.Story**: `[name, title, photo, highlight1, highlight2, highlight3, student_id, age]`
- **story.StoryAnswer**: `[question, answer, story]`
- **story.StoryCourse**: `[name, short_name, sort, flag, objects, active_objects]`
- **story.StoryPurpose**: `[name, short_name, sort, flag, objects, active_objects]`
- **story.StoryQuestion**: `[question, category, type, sort, flag, word_limit, objects, active_objects]`
- **story.StoryQuestionCategory**: `[category, sort]`
- **story.StoryQuestionChoice**: `[question, choice, sort]`
- **story.StoryTags**: `[story, tag, sort]`
- **story.Work**: `[name, kana, displayed_name, student_id, work_type, work_types, url, work_name]`
- **story.WorkIndustry**: `[name, short_name, sort, flag, objects, active_objects]`
- **story.WorkSoftware**: `[name, short_name, sort, flag, objects, active_objects]`
- **story.WorkType**: `[type, eng_name, sort, flag, objects, active_objects]`
- **users.Profile**: `[user, name, kana, gender, pic, birthday, summary]`
- **users.UserEmail**: `[user, email, is_confirmed, is_primary]`
- **users.UserSession**: `[user, session]`

### 🔗 RELATIONSHIPS
- analytics.ContactAccounts -> DepartmentCategory
- analytics.ContactAccounts -> PositionCategory
- analytics.ContactAccounts -> corporate.Corporation
- analytics.FinanceImage -> ProjectFinance
- analytics.GAData -> GAClient
- analytics.GAData -> GAKeyword
- analytics.GAData -> GALandingPageURL
- analytics.GAData -> GAMedium
- analytics.GAData -> GAPageURL
- analytics.GAData -> GASource
- analytics.GASales -> GAData
- analytics.Negotiations -> ContactAccounts
- analytics.Negotiations -> NegoTrainingTheme
- analytics.Negotiations -> NegoTrainingType
- analytics.Negotiations -> corporate.Competitor
- analytics.Negotiations -> corporate.Corporation
- analytics.Negotiations -> corporate.InterviewState
- analytics.Negotiations -> corporate.Training
- analytics.Negotiations -> corporate.TrainingBill
- analytics.Negotiations -> customer.Infra

## 📂 DIRECTORY STRUCTURE
```
├── README.md
├── __init__.py
├── bohr/
  ├── __init__.py
  ├── apps/
    ├── __init__.py
    ├── bohr_core/
    ├── contest/
    ├── quiz/
    ├── student/
  ├── email/
    ├── email_doc_apply_edu.py
    ├── email_doc_apply_enroll.py
    ├── email_doc_apply_staff.py
    ├── email_otp.py
    ├── email_transfer.py
    ├── email_verify.py
  ├── email_data.py
  ├── templates/
    ├── bohr_common/
    ├── bohr_core/
    ├── contest/
    ├── error.html
    ├── member/
    ├── mobile_app/
    ├── od/
    ├── quiz/
    ├── student/
  ├── utils.py
├── bohr_api/
  ├── __init__.py
  ├── apps.py
  ├── email/
    ├── cancel_email.py
    ├── email_data.py
    ├── email_doc_apply_attendance.py
    ├── email_doc_apply_edu.py
    ├── email_doc_apply_enroll.py
    ├── email_doc_apply_reskill.py
    ├── email_doc_apply_staff_attendance.py
    ├── email_doc_apply_staff_edu.py
    ├── email_doc_apply_staff_enroll.py
    ├── email_doc_apply_staff_reskill.py
    ├── email_otp.py
    ├── email_transfer.py
    ├── email_verify.py
  ├── functions.py
  ├── migrations/
    ├── __init__.py
  ├── models.py
  ├── query_debugger.py
  ├── serializers.py
  ├── urls.py
  ├── utils.py
  ├── views.py
├── bohr_common/
  ├── __init__.py
  ├── apps.py
  ├── functions.py
  ├── migrations/
    ├── __init__.py
  ├── models.py
  ├── serializers.py
  ├── urls.py
  ├── views/
    ├── IT_test.py
    ├── __init__.py
├── bohr_corp/
  ├── __init__.py
  ├── apps.py
  ├── constants.py
  ├── functions_admin.py
  ├── functions_common.py
  ├── functions_inst.py
  ├── functions_student.py
  ├── helpers.py
  ├── migrations/
    ├── __init__.py
  ├── processes.py
  ├── serializers_renewal.py
  ├── urls.py
  ├── views_admin.py
  ├── views_common.py
  ├── views_inst.py
  ├── views_student.py
  ├── watch_history_migration.py
├── chat/
  ├── __init__.py
  ├── admin.py
  ├── apps.py
  ├── migrations/
    ├── 0001_initial.py
    ├── __init__.py
  ├── models.py
  ├── templates/
    ├── chat/
  ├── tests.py
  ├── urls.py
  ├── utils.py
  ├── views.py
├── chatbot_credentials.json
├── common/
  ├── apps/
    ├── digital_text/
  ├── templates/
    ├── digital_text/
├── corp/
  ├── apps/
    ├── corporation/
  ├── templates/
    ├── corporation/
├── coupon_calc_script.py
├── doc/
  ├── permissions.txt
  ├── setup
├── documentation_website/
  ├── __init__.py
  ├── init.py
  ├── urls.py
  ├── views.py
├── formats/
  ├── __init__.py
  ├── en/
    ├── __init__.py
    ├── formats.py
├── get-pip.py
├── kikuichimonji/
  ├── __init__.py
  ├── apps/
    ├── __init__.py
    ├── analytics/
    ├── contact/
    ├── contract/
    ├── core/
    ├── corporate/
    ├── customer/
    ├── data_analysis/
    ├── equipment/
    ├── event/
    ├── exam/
    ├── ia_admin/
    ├── instructor/
    ├── job_outsourcing/
    ├── knowledge_centre/
    ├── library/
    ├── maintenance/
    ├── payment/
    ├── performance/
    ├── price/
    ├── qasystem/
    ├── questionnaire/
    ├── reservation/
    ├── school/
    ├── staff/
    ├── stories/
    ├── story/
  ├── middleware.py
  ├── settings.py
  ├── settings_local.py
  ├── settings_local.py:Zone.Identifier
  ├── templates/
    ├── 404_error.html
    ├── admin_base.html
    ├── analytics/
    ├── base.html
    ├── contact/
    ├── contract/
    ├── core/
    ├── corporate/
    ├── customer/
    ├── date_range.html
    ├── empty.html
    ├── equipment/
    ├── event/
    ├── exam/
    ├── ia_admin/
    ├── instructor/
    ├── job_outsourcing/
    ├── knowledge_centre/
    ├── library/
    ├── maintenance/
    ├── message.html
    ├── navbars/
    ├── pagination.html
    ├── pagination2.html
    ├── payment/
    ├── performance/
    ├── price/
    ├── qasystem/
    ├── questionnaire/
    ├── registration/
    ├── reservation/
    ├── school/
    ├── staff/
    ├── stories/
    ├── story/
    ├── sub_nav.html
    ├── sub_nav_applications.html
    ├── sub_nav_corp.html
    ├── sub_nav_corp_training.html
    ├── sub_nav_job_out.html
    ├── sub_nav_maintenance_modif.html
  ├── test.py
  ├── urls.py
  ├── utils/
    ├── api_permision.py
    ├── choices.py
    ├── excel_export.py
    ├── forms.py
    ├── initial_data.py
    ├── message_types.py
    ├── utils.py
    ├── widgets.py
  ├── wsgi.py
├── logs/
├── manage.py
├── mem/
  ├── media/
    ├── ckeditor/
    ├── corp/
    ├── notifications/
    ├── pdf_file_appli/
├── migrate_db.py
├── migrate_work_to_document_upload.py
├── pyproject.toml
├── requirements/
  ├── dev.txt
  ├── old_dev.txt
  ├── old_prod.txt
  ├── old_staging.txt
  ├── prod.txt
  ├── staging.txt
├── scripts/
  ├── add_catchup_playlist_type.py
  ├── course_model_migrations.py
  ├── documentation_reload.sh
  ├── macos_restore_db_backup.sh
  ├── make_db_backup.sh
  ├── member_merge_migrate.sh
  ├── restore_db_backup.sh
  ├── test_server_restore_db_from_backup.sh
├── scripts.py
├── setup.txt
├── static/
  ├── admin/
    ├── css/
    ├── data_files/
    ├── fonts/
    ├── img/
    ├── js/
  ├── bohr/
    ├── common_bohr/
  ├── chat/
    ├── css/
    ├── images/
    ├── js/
  ├── ckeditor/
    ├── ckeditor/
    ├── ckeditor-init.js
    ├── ckeditor_uploader/
    ├── file-icons/
    ├── galleriffic/
  ├── corp/
    ├── common/
  ├── css/
    ├── beta.css
    ├── cancel_doc.css
    ├── common.css
    ├── common_old[.css
    ├── print.css
    ├── print2.css
    ├── redmond/
  ├── font/
    ├── -F6jfjtqLzI2JPCgQBnw7HFyzSD-AsregP8VFBEj75vY0rw-oME.ttf
    ├── NotoSansJP-Regular.ttf
  ├── fontawesome-5.15.2/
    ├── LICENSE.txt
    ├── attribution.js
    ├── css/
    ├── js/
    ├── less/
    ├── metadata/
    ├── scss/
    ├── sprites/
    ├── svgs/
    ├── webfonts/
  ├── fullcalendar-5.4.0/
    ├── LICENSE.txt
    ├── README.md
    ├── examples/
    ├── lib/
  ├── images/
    ├── IA_logo_hankou.PNG
    ├── IBJ_logo_hankou.PNG
    ├── Thumbs.db
    ├── beta/
    ├── dload.gif
    ├── down.gif
    ├── down_no.gif
    ├── eq.gif
    ├── eq_no.gif
    ├── face/
    ├── hanko.PNG
    ├── internet_academy_address.PNG
    ├── link.gif
    ├── list.gif
    ├── list2.gif
    ├── logo.gif
    ├── logo_bk.gif
    ├── sort_asc.gif
    ├── sort_desc.gif
    ├── sp.gif
    ├── spacer.gif
    ├── stars/
    ├── up.gif
    ├── up_no.gif
  ├── js/
    ├── common.js
    ├── datepicker.js
    ├── firebase-messaging-sw.js
    ├── init.js
    ├── jquery-ui-1.10.4.custom.min.js
    ├── tools.js
  ├── library/
  ├── models/
    ├── face_detection_yunet_2023mar.onnx
  ├── nested_admin/
    ├── dist/
    ├── src/
  ├── price/
    ├── images/
  ├── rest_framework/
    ├── css/
    ├── docs/
    ├── fonts/
    ├── img/
    ├── js/
  ├── skill_check/
    ├── css/
  ├── tagify/
    ├── css/
    ├── js/
├── users/
  ├── __init__.py
  ├── admin.py
  ├── apps.py
  ├── migrations/
    ├── 0001_initial.py
    ├── __init__.py
  ├── models.py
  ├── views.py
### 🌌 L4 SEMANTIC INTENT MAP (Core Hubs)
- **users/**: Centralized Identity Management. Handles Profiles, secondary emails, and session persistence.
- **chat/**: Real-time Communication Engine. Manages Rooms, Participants, and message history.
- **bohr_api/**: Primary Frontend Bridge. Acts as the API gateway for the Bohr-Individual Vue frontend.
- **kikuichimonji/apps/**: The "Enterprise Core." Contains dozens of specialized modules for school management, reservations, and analytics.
- **bohr_corp/**: Corporate Trainee Logic. Handles IP-restricted access and corporate-specific training workflows.
