*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open test browser
Suite Teardown  Close all browsers

*** Test cases ***

Test Strip
    # XXX: under Plone 4.2 is fieldsetlegend-0 instead of fieldsetlegend-categorization
    [Tags]  Expected Failure

    Enable Autologin as  Site Administrator
    Go to  ${PLONE_URL}

    Open Add New Menu
    Click Link  css=a#dexteritytest
    Page Should Contain  Add dexterityTest
    Log Source
    Click Link  css=a#fieldsetlegend-categorization
    Add Subject  \ testing this \ \
    Focus  css=a#fieldsetlegend-categorization
    Press Key  css=a#fieldsetlegend-categorization  \13
    Set Selenium Timeout  3s
    ${subject}  Get Text  css=li.token-input-token-facebook:first-child p
    Should Be True  '${subject}' != ' testing this '

*** Keywords ***

Add Subject
    [arguments]  ${title}
    Input Text  css=#token-input-form-widgets-IDublinCore-subjects  ${title}
