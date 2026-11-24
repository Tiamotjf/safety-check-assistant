# Lab 2 worksheet

Use this file for the written notes in all five phases. The Canvas page gives the instructions. This is the only Markdown file you need to complete. You do not need to write paragraphs.

## What to do

Work through the five phases on the Canvas page:

1. Write one inference about what the system senses, infers and does.
2. Draw the interaction flow as a loop from the person's goal to system feedback.
3. Draw the normal interaction as a storyboard with as many moments as you need.
4. Show what happens when the inference is wrong and how the person recovers.
5. Choose one design check and draw an improvement into the storyboard.

## 1. Your interaction

**Problem from Lab 1:**

People using AI agents to complete tasks may struggle to identify unsafe actions because the agent's planned actions, tool use, and data access are not always clear before execution.

**What should the system sense, infer and do?**

- **Sense:** The user's request, the agent's planned action, the tool being used, the recipient or destination, and the data that may be accessed or shared.
- **Infer:** Whether the planned action may expose sensitive information or cause an unintended consequence.
- **Do:** If the action may be risky, pause it and show a warning panel with the planned action, relevant data, and a short reason for the warning. Let the user approve, edit, or cancel before the action is executed.
- **Channel:** A warning and confirmation panel in the AI agent's app interface.

**When could that inference be wrong?**

The system may flag a safe action as risky, or fail to notice a real risk because it misunderstands the context or misses sensitive information. For example, it may not know that an email recipient is trusted, or it may overlook personal information in an attachment.

## 2. Your flow

**Person's goal:** Use an AI agent to complete a task, such as sending a document by email.

**What the system senses:** The request, planned action, recipient, attachment, tool, and data that will be shared.

**What the system infers:** The action may be risky because the attachment could contain sensitive information or the recipient may be incorrect.

**What the system does and through which channel:** The agent pauses before sending and displays a warning panel in the app. The panel shows the recipient, attachment, reason for concern, and **Approve**, **Edit**, and **Cancel** options.

**What feedback the person receives:** The person sees the warning and chooses what to do. The system then confirms whether the email was sent, edited, or cancelled. The feedback informs the person's next step, completing the loop back to their goal.

## 3. Your normal-interaction storyboard

1. **User goal:** The user asks the AI agent to email a document to a colleague.
2. **Agent prepares the action:** The agent drafts the email and selects the recipient and attachment.
3. **Safety check:** The system checks the recipient, attachment, and planned action before sending.
4. **Warning shown:** The system displays the planned action and explains why the attachment may contain sensitive information.
5. **User decides:** The user checks the details and chooses **Approve**, **Edit**, or **Cancel**.
6. **Result and feedback:** The agent carries out the selected action and shows a clear confirmation message. The user can continue their task.

## 4. Your failure-and-recovery storyboard

- **What wrong inference does it make?** The system incorrectly judges a safe email to a trusted colleague as risky, or it fails to identify sensitive information in an attachment.
- **How does the person notice?** The person checks the recipient, attachment, and explanation shown in the warning and notices that the system's assessment does not match the situation.
- **How do they recover?** The person can edit the recipient or attachment, cancel the action, or approve it after reviewing the details. The system should not silently execute a potentially high-risk action.
- **What should the system learn?** The system should use corrections as feedback where appropriate, improve its context checks, and explain uncertainty. It should not assume that one approval means all similar future actions are safe.

## 5. Check the storyboard with a secondary user

- **Which question did you choose?** Is it apparent why the system acted?
- **Which frame did you change?** Frame 4 of the normal-interaction storyboard, where the warning is shown.
- **What was unclear?** A secondary user who is unfamiliar with AI agents may not understand technical security terms or why the system paused the email.
- **What did you change and why?** I added a plain-language explanation, clearly displayed the recipient and attachment, and used simple **Approve**, **Edit**, and **Cancel** buttons. This helps the secondary user understand the reason for the warning and make an informed decision.

## Save

Save this completed worksheet with the required image files. Use fictional examples and do not include real names, faces, private messages, or confidential information.
