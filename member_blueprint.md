# REPO BLUEPRINT: blueprint_sync_member

## 🏗 DATA MODELS (291 discovered)
- **analytics.CounselingSalesBar**: `[sales]`
- **analytics.FinanceImage**: `[image, report]`
- **analytics.GAClient**: `[ga_id]`
- **analytics.GAData**: `[date, client, source, medium, keyword, page_url, landing_page_url]`
- **analytics.GAKeyword**: `[short_name, sort, flag]`
- **analytics.GALandingPageURL**: `[url, sort, flag]`
- **analytics.GAMedium**: `[name, short_name, sort, flag]`
- **analytics.GAPageURL**: `[url, sort, flag]`
- **analytics.GASales**: `[ga_data, actual_sales]`
- **analytics.GASource**: `[name, short_name, sort, flag]`
- **analytics.ProjectFinance**: `[project, implementatin_details, increased_sales, increased_cost]`
- **analytics.ProjectMiddleReport**: `[project, details, verify_start, verify_end, inspection_deadline, result]`
- **analytics.ProjectProfile**: `[name, incharge, verify_start, verify_end, inspection_deadline, details, expected_sales, expected_cost]`
- **analytics.ProjectProfileImage**: `[image, report]`
- **analytics.ProjectUpdateHistory**: `[staff, project, time, changes]`
- **analytics.ReportImage**: `[image, report]`
- **analytics.WebPage**: `[create_staff, title, url, update_staff, create_date, update_date]`
- **chat.ChatUser**: `[user, pic, name, type, created_at, objects, unread_messages]`
- **chat.ChatUserManager**: `[chat_user, chat_user]`
- **chat.Message**: `[room, chat_user, message, created_at, created_at]`
- **chat.Participant**: `[room, chat_user, unread_messages, created_at]`
- **chat.Room**: `[name, pic, last_message, platform, private, participant_count, created_at, objects]`
- **chat.RoomManager**: `[room, room, room]`
- **contact.Email**: `[title, body, time, type, sent_to, seen_by, total]`
- **contact.EmailType**: `[name, short_name, sort, flag]`
- **contact.Notice**: `[type, date, title, body, ext_url, push_notification_sent, is_active, history]`
- **contact.NoticeType**: `[name, short_name, sort, flag, active_objects, objects]`
- **contact.Notification**: `[creation_date, time, updated_on, type, destination, title, body, body_email]`
- **contact.NotificationType**: `[name, short_name, sort, flag]`
- **contest.Contest**: `[title, is_active, description, requirements_file, settings, vote_list, start_time, submission_end_time]`
- **contest.Product**: `[user, title, description, picture, file, counter, tags, contest]`
- **contest.Tag**: `[title]`
- **contract.BenefitContact**: `[contract, staff, state, note, time]`
- **contract.BenefitContactState**: `[name, short_name, sort, flag, objects, active_objects]`
- **contract.BenefitTarget**: `[course, course_price, course_num, course_term, sort, flag, objects, active_objects]`
- **contract.ChangeContract**: `[contract, date, price, tax_rate, entrance_pay_price, tuition_pay_price, reduce_reason, benefit_entrance_pay_price]`
- **contract.Contract**: `[customer, type, date, first_time, first_branch, first_class_type, first_class, first_class_num]`
- **contract.ContractCancelType**: `[name, short_name, sort, flag, objects, active_objects]`
- **contract.ContractType**: `[name, short_name, sort, flag, objects, active_objects]`
- **core.AccessLog**: `[user, sub_category, time, flag]`
- **core.Base**: `[consumption_tax, entrance_pay_price, bohr_base_url]`
- **core.BulletinBoardMessage**: `[date, sender, receiver, message, time_limit]`
- **core.CalendarHolidays**: `[year, dates]`
- **core.Category**: `[name, nav, sort, flag, objects, active_objects]`
- **core.CronMail**: `[cron_type, instruction, subject, body]`
- **core.HolidayDates**: `[date]`
- **core.IA**: `[date_yyyymm, goal_price, sum_cost, maintenance_list, holiday_list, day_num, target_branch_num, target_online_num]`
- **core.Ipaddress**: `[ip_address, flag]`
- **core.Mail**: `[material_address, lesson_address, material_title, material_body]`
- **core.Nav**: `[name, short_name, link, sort, flag, objects, active_objects]`
- **core.SubCategory**: `[category, name, link, allow_user, allow_group, sort, flag, objects]`
- **corporate.Assignment**: `[training, title, deadline, notes]`
- **corporate.AssignmentSubmission**: `[assignment, corp_account, file, time]`
- **corporate.Attendance**: `[training, corp_account, training_schedule, fill_time, last_login, note]`
- **corporate.CorpAccounts**: `[corporation, user, is_admin, password, name, kana, email, email_verified]`
- **corporate.CorpCall**: `[corporation, staff, note, time, mail_body, mail_from, mail_sent_to, mail_cc_to]`
- **corporate.CorpClassProgress**: `[corp_account, class_name, progress, completed_progress_time, flag, active_objects, objects]`
- **corporate.CorpClasses**: `[name, short_name, lesson_num, sort, flag, objects, active_objects]`
- **corporate.CorpImpression**: `[corp_account, training, training_schedule, name, impress_point1, impress_point2, impress_point3, impress_note]`
- **corporate.CorpImpressionOD**: `[corp_account, training, lesson, playlist, video, impress_point1, impress_point2, impress_point3]`
- **corporate.CorpIndustryType**: `[name, short_name, parent, flag, sort]`
- **corporate.CorpIndustryTypeCat**: `[name, short_name, flag, sort]`
- **corporate.CorpListing**: `[name, short_name, flag, sort]`
- **corporate.CorpPlaylistProgress**: `[corp_account, playlist, progress, flag, active_objects, objects]`
- **corporate.CorpStaffType**: `[name, short_name, sort, flag]`
- **corporate.CorpState**: `[name, short_name, sort, flag, objects, active_objects]`
- **corporate.CorpSubsidyType**: `[name, short_name, flag, sort]`
- **corporate.CorpVideoProgress**: `[corp_account, video, video_num, class_name, lesson_num, progress, watched, count]`
- **corporate.CorporateAnswers**: `[question, title, is_correct, text, text, text]`
- **corporate.CorporateCommonSettings**: `[classes_note, note_admin]`
- **corporate.CorporateExamSettings**: `[short_name, no_of_ques, random_question_order, random_answer_order, pass_percent, time_limit, retake_time]`
- **corporate.CorporateQuestions**: `[create_time, title, class_name, lesson_name, total_taken, total_correct, mini_exam_flag, final_exam_flag]`
- **corporate.CorporateSubmission**: `[corp_account, class_name, lesson_name, exam_type, training, start_time, end_time, score]`
- **corporate.CorporateUpdateHistory**: `[staff, corporation, training, time, page_updated, changes]`
- **corporate.Corporation**: `[name, first_name, url, kana, gender, birth_yyyymmdd, state, staff]`
- **corporate.CorporationCron**: `[name, staff, time]`
- **corporate.CustomizedSkill**: `[training, skill, sort]`
- **corporate.EmailToCorp**: `[title, body, time, email_from, sent_to, cc_to, Bcc_to, seen_by]`
- **corporate.EmployeesNumberRange**: `[name, short_name, flag, sort]`
- **corporate.EnvironmentManualSetting**: `[training, name, software_name, url, remarks, flag, note_student]`
- **corporate.EnvironmentSetting**: `[name, url, default, sort]`
- **corporate.GrantName**: `[name, short_name, flag]`
- **corporate.GrantStyle**: `[name, short_name, flag]`
- **corporate.InterviewState**: `[name, short_name, sort, flag, objects, active_objects]`
- **corporate.ItSkill**: `[name, short_name, sort, flag, objects, active_objects]`
- **corporate.ODReminderEmail**: `[training, type, frequency, body, flag, objects, active_objects]`
- **corporate.QAReport**: `[parent, corp_account, training, lesson, title, content, time]`
- **corporate.Reaction**: `[user, report, emoji]`
- **corporate.Report**: `[parent, corp_account, training, title, content, time, seen_by, data]`
- **corporate.ServiceMode**: `[name, short_name, flag, sort]`
- **corporate.SkillConfig**: `[training, skill_check_flag, customized_flag, comment_flag, skill_low_flag, skill_avg_flag, show_ranking, random_question_order]`
- **corporate.Subsidy**: `[training, grant_name, grant_style, corp_accounts, file, company, address, time]`
- **corporate.SubsidyHistory**: `[subsidy, time, status]`
- **corporate.TextbookManual**: `[training, name, software_name, url, remarks, flag, note_student]`
- **corporate.TraineeComment**: `[corp_account, training, comment, staff]`
- **corporate.TraineeCustomizedSkill**: `[corp_account, customized_skill, score]`
- **corporate.Training**: `[corporation, category, skill_level, instruction_skill, corp_accounts, mode, title, type]`
- **corporate.TrainingBill**: `[training, contract_date, tuition_pay_price, tax_rate, sale_tax, amount_of_payment]`
- **corporate.TrainingCategory**: `[name]`
- **corporate.TrainingDefaultReminder**: `[title, note, sort, flag, objects, active_objects]`
- **corporate.TrainingMode**: `[name, short_name, sort, flag, objects, active_objects]`
- **corporate.TrainingNote**: `[name, content]`
- **corporate.TrainingNotice**: `[training, notice, created_at, updated_at]`
- **corporate.TrainingReminder**: `[training, deadline, title, remind_staff, note, finished, created_at, created_by_staff]`
- **corporate.TrainingReport**: `[training, name, file, updated_by, updated_at, created_at, display]`
- **corporate.TrainingSchedule**: `[training, date, start_time, end_time, title, url, location, contents]`
- **corporate.TrainingTextbook**: `[class_name, url, note_student, note, flag, sort]`
- **corporate.TrainingType**: `[name, short_name, sort, flag, objects, active_objects]`
- **customer.BenefitType**: `[name, short_name, flag, sort]`
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
- **customer.Customer**: `[user, name, kana, gender, birth_yyyymmdd, state, status, student_id]`
- **customer.CustomerPosition**: `[name, short_name, flag, sort]`
- **customer.CustomerStats**: `[customer, date, ondemand_count, ondemand_time, latest_ondemand_time, m2m_count, m2m_time, latest_m2m_time]`
- **customer.CustomerTarget**: `[name, short_name, flag, sort]`
- **customer.CustomerUpdateHistory**: `[staff, customer, time, page_updated, changes]`
- **customer.IndustryType**: `[name, short_name, flag, sort]`
- **customer.Infra**: `[name, short_name, sort, flag, objects, active_objects]`
- **customer.Media**: `[name, short_name, list_flag, sort, flag, objects, active_objects]`
- **customer.MovieType**: `[name, flag, sort]`
- **customer.Occupation**: `[name, short_name, flag, sort]`
- **customer.PreviousJobTitle**: `[name, short_name, flag, sort]`
- **customer.Purpose**: `[name, short_name, flag, sort]`
- **customer.ReferralMatch**: `[inviter, invitee, gift_sent_flag, date_add, date]`
- **customer.ReskillEnd**: `[update_time, date_of_issue, customer, zipcode, address, name, kana, custom_start_date]`
- **customer.ReskillHalf**: `[update_time, date_of_issue, customer, zipcode, address, name, kana, custom_start_date]`
- **customer.ReskillUnemployment**: `[update_time, date_of_issue, customer, name, custom_start_date, custom_end_date, remark, same_address]`
- **customer.TenureStatus**: `[name, short_name, flag, sort]`
- **customer.TopMessage**: `[title, message, sort, start_timing, percentage, condition, end_timing, display_period]`
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
- **exam.ExamAttend**: `[exam_schedule, customer, staff, time, note, os, points, result]`
- **exam.ExamSchedule**: `[exam, date, begin_hhii, end_hhii, branch, classroom, note, max_num]`
- **exam.ExamType**: `[name, short_name, sort, flag, objects, active_objects]`
- **exam.Skill**: `[customer, type, time, question_num, right_min_num, right_num, result]`
- **exam.SkillAnswers**: `[question, num, name, right_flag, flag, objects, active_objects]`
- **exam.SkillQuestions**: `[skill_type, num, name, flag, objects, active_objects]`
- **exam.SkillType**: `[name, short_name, question_num, right_min_num, sort, flag, objects, active_objects]`
- **exam.StudentExam**: `[name, short_name, exam_type, sort, flag, objects, active_objects]`
- **ia_admin.IndAnswer**: `[question, answer, quiz]`
- **ia_admin.IndQuizSetting**: `[type, class_name, lesson_name, no_of_ques, random_question_order, random_answer_order, pass_percent, time_limit]`
- **ia_admin.QuizTaken**: `[customer, start, end, class_name, lesson_name, exam_type, setting, score]`
- **instructor.Certification**: `[name, name_ja, short_name, sort, flag]`
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
- **quiz.SittingManager**: `[questions, question_order, new_sitting]`
- **quiz.Topic**: `[topic_group, name, short_name]`
- **quiz.TopicGroup**: `[name, short_name]`
- **school.ApplyGroup**: `[name, short_name, sort, flag, active_objects, objects]`
- **school.ApplyStatus**: `[name, short_name, sort, flag]`
- **school.ApplyType**: `[group, name, data, short_name, sort, flag]`
- **school.AttendClass**: `[customer, schedule, m2m, date, branch, classroom, freeroom, classroom_period]`
- **school.AttendFlag**: `[name, short_name, sort, flag, objects, active_objects]`
- **school.Category**: `[name, short_name, sort, flag]`
- **school.Class**: `[name, short_name, lesson_num, group, point_num, tuition_pay_price, sort, flag]`
- **school.ClassGroup**: `[name, point_num, tuition_pay_price, sort, flag, objects, active_objects]`
- **school.ClassLesson**: `[lesson_class, num, max_seats, extra_lesson, video_duration, lesson_material, objects, active_objects]`
- **school.ClassProgress**: `[customer, class_name, class_od_progress, completed_od_prog_date, homework_od_progress, sort, flag, lesson_ids_watched]`
- **school.ClassType**: `[name, short_name, color, sort, flag, objects, active_objects]`
- **school.CorporateCategory**: `[name, short_name, sort, flag]`
- **school.Course**: `[name, short_name, classes, point_num, tuition_pay_price, sort, flag, objects]`
- **school.CurSheet**: `[staff, file, cur_sheet_class, cur_sheet_class_num, point, time, edit_time]`
- **school.DocumentApply**: `[date, customer, apply_time, apply_type, status, reserved_date, reserved_time, name]`
- **school.ITgreeting**: `[date, type, ip, a1, a2, a3, result]`
- **school.ImpressionOD**: `[customer, lesson, staff, playlist, video, impress_point1, impress_point2, impress_point3]`
- **school.M2M**: `[customer, custom_tel_num, m2m_type, m2m_class, m2m_class_num, os, request_staff, request_date]`
- **school.M2MBranch**: `[name, sort, flag, objects, active_objects]`
- **school.M2MCheckItems**: `[type, title, sort, flag, active_objects, objects]`
- **school.M2MCheckTypes**: `[name, short_name, sort, flag, active_objects, objects]`
- **school.M2MContact**: `[m2m, type, note, staff, time]`
- **school.M2MContactType**: `[name, short_name, sort, flag, objects, active_objects]`
- **school.M2MControl**: `[name, short_name, sort, flag, objects, active_objects]`
- **school.M2MEmail**: `[customer, title, body, time, type, contact, is_seen]`
- **school.M2MEmailTemplate**: `[name, type, subject, body]`
- **school.M2MFeedback**: `[m2m, assignment, message, instructor_note, created_at]`
- **school.M2MSchedule**: `[date1, begin_hhii1, end_hhii1, date2, begin_hhii2, end_hhii2, date3, begin_hhii3]`
- **school.M2MState**: `[name, short_name, sort, flag, objects, active_objects]`
- **school.M2MTime**: `[num, begin_hhii, end_hhii, note]`
- **school.M2MType**: `[name, short_name, sort, flag, objects, active_objects]`
- **school.Material**: `[filename, file, material_type, staff, sort, flag, time]`
- **school.MaterialType**: `[name, short_name, sort, flag]`
- **school.NPSsurvey**: `[customer, referral_point, note, query, location, created_at, reject_flag]`
- **school.NPSsurveyLocation**: `[name, short_name, flag]`
- **school.OdLog**: `[customer, video, od_class, od_class_num, od_video_num, count, time]`
- **school.OndemandPopup**: `[date_s, date_e, title, content, created_staff, time, display]`
- **school.Opinion**: `[customer, custom_name, custom_staff, report_staff, happen_time, send_time, type, level]`
- **school.OpinionLevel**: `[num, name, sort, flag, objects, active_objects]`
- **school.OpinionResultType**: `[name, short_name, sort, flag, objects, active_objects]`
- **school.OpinionType**: `[name, short_name, sort, flag, objects, active_objects]`
- **school.PlayList**: `[title, instructor, lesson_name, group_name, sort, type, is_active, note_of_video]`
- **school.PlaylistProgress**: `[customer, playlist, playlist_od_progress, sort, flag, active_objects, objects]`
- **school.PlaylistType**: `[name, short_name, sort, flag, active_objects, objects]`
- **school.Procedure**: `[customer, staff, point_date, procedure_name, contract, contract_point_num, cross_contract, cross_contract_point_num]`
- **school.ProcedureName**: `[name, short_name, point_num, sort, flag, objects, active_objects]`
- **school.Reception**: `[customer, date, branch, class_staff, post_time, impress_point1, impress_note]`
- **school.RoutineFile**: `[date, routine_type, file, staff, objects, active_objects]`
- **school.RoutineType**: `[name, short_name, sort, flag, objects, active_objects]`
- **school.ScheduleClass**: `[date, classroom, classroom_period, lesson, staff, url, start_time]`
- **school.Video**: `[playlist, name, url, section, duration, sort, is_extra]`
- **school.VideoGroup**: `[name, text, sort, is_active]`
- **school.VideoProgress**: `[customer, video, video_od_progress, watched, count, sort, flag, active_objects]`
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
- **story.StoryQuestion**: `[question, category, type, sort, flag, objects, active_objects, student_objects]`
- **story.StoryQuestionCategory**: `[category, sort]`
- **story.StoryQuestionChoice**: `[question, choice, sort]`
- **story.StoryTags**: `[story, tag, sort]`
- **story.Work**: `[name, kana, displayed_name, student_id, work_type, url, work_name, date]`
- **story.WorkIndustry**: `[name, short_name, sort, flag, objects, active_objects]`
- **story.WorkSoftware**: `[name, short_name, sort, flag, objects, active_objects]`
- **story.WorkType**: `[type, sort, flag, objects, active_objects]`
- **users.Profile**: `[user, name, kana, gender, pic, birthday, summary]`
- **users.UserEmail**: `[user, email, is_confirmed, is_primary]`
- **users.UserSession**: `[user, session]`

### 🔗 RELATIONSHIPS
- analytics.FinanceImage -> ProjectFinance
- analytics.GAData -> GAClient
- analytics.GAData -> GAKeyword
- analytics.GAData -> GALandingPageURL
- analytics.GAData -> GAMedium
- analytics.GAData -> GAPageURL
- analytics.GAData -> GASource
- analytics.GASales -> GAData
- analytics.ProjectProfile -> staff.Staff
- analytics.ProjectProfileImage -> ProjectProfile
- analytics.ProjectUpdateHistory -> staff.Staff
- analytics.ReportImage -> ProjectMiddleReport
- analytics.WebPage -> staff.Staff
- chat.Message -> ChatUser
- chat.Message -> Room
- chat.Participant -> ChatUser
- chat.Participant -> Room
- chat.Room -> Message
- contact.Email -> EmailType
- contact.Notice -> NoticeType

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
  ├── admin.py
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
  ├── tests.py
  ├── urls.py
  ├── utils.py
  ├── views.py
├── bohr_common/
  ├── __init__.py
  ├── admin.py
  ├── apps.py
  ├── functions.py
  ├── migrations/
    ├── __init__.py
  ├── models.py
  ├── serializers.py
  ├── tests.py
  ├── urls.py
  ├── views/
    ├── IT_test.py
    ├── __init__.py
├── bohr_corp/
  ├── __init__.py
  ├── admin.py
  ├── apps.py
  ├── functions.py
  ├── migrations/
    ├── __init__.py
  ├── models.py
  ├── serializers.py
  ├── tests.py
  ├── urls.py
  ├── views.py
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
├── doc/
  ├── permissions.txt
  ├── setup
├── documentation_website/
├── formats/
  ├── en/
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
  ├── settings.py
  ├── settings_local.py
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
    ├── maintenance/
    ├── message.html
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
    ├── choices.py
    ├── forms.py
    ├── initial_data.py
    ├── message_types.py
    ├── utils.py
    ├── widgets.py
  ├── wsgi.py
├── logs/
├── manage.py
├── mem/
├── migrate_db.py
├── requirements/
  ├── dev.txt
  ├── prod.txt
  ├── staging.txt
├── setup.txt
├── users/
  ├── __init__.py
  ├── admin.py
  ├── apps.py
  ├── migrations/
    ├── 0001_initial.py
    ├── __init__.py
  ├── models.py
  ├── tests.py
  ├── views.py
```