# REPO BLUEPRINT: bohr-individual

## 🛠 TECH STACK: Go, Node.js/Frontend

### 🛣 GO ROUTES (L2)
- **support.go**: `[SupportRoutes]`
- **itTest.go**: `[ITTestRoutes]`
- **submission.go**: `[SetupSubmissionRoutes]`
- **routes.go**: `[SetupRoutes]`
- **notification.go**: `[NotificationRoutes]`
- **user.go**: `[UserRoutes]`
- **auth.go**: `[AuthRoutes]`
- **reservation.go**: `[ReservationRoutes]`
- **od.go**: `[ODRoutes]`

### 🌐 API CONSUMPTION (L3 - Vue/TS)
- **BenefitApplication.vue** -> imports: `[@/api/benefit]`
- **BenefitApplicationStatus.vue** -> imports: `[@/api/benefit]`
- **BenefitMyPage.vue** -> imports: `[@/api/benefit]`
- **BenefitOtherApplication.vue** -> imports: `[@/api/benefit]`
- **CertificationExamHistory.vue** -> imports: `[@/api/certificationExam]`
- **CertificationExamRegistration.vue** -> imports: `[@/api/certificationExam]`
- **DataSubmissionPage.vue** -> imports: `[@/api/data]`
- **EnvironmentTools.vue** -> imports: `[../api/od]`
- **FAQPage.vue** -> imports: `[@/api/help]`
- **ITTest.vue** -> imports: `[../api/itTest, ../api/skillTest]`
- **ITTestResult.vue** -> imports: `[@/api/skillTest, @/api/itTest]`
- **JobSearch.vue** -> imports: `[@/api/job]`
- **LearningSpaceReservations.vue** -> imports: `[@/api/reservation]`
- **LiveReservationPage.vue** -> imports: `[@/api/reservation]`
- **NotificationPanel.vue** -> imports: `[@/api/notification]`
- **ODTable.vue** -> imports: `[../api/od]`
- **ODVideoPage.vue** -> imports: `[@/api/od]`
- **ProfileEdit.vue** -> imports: `[@/api/user]`
- **ProfilePage.vue** -> imports: `[../api/user]`
- **ReservationEvaluationPopup.vue** -> imports: `[@/api/reservation]`

## 📂 DIRECTORY STRUCTURE (L2)
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