# Bob Workshop

## 0. Setup
1. Download installer from [https://bob.ibm.com/download](https://bob.ibm.com/download)

2. Install Bob and try log in

## Lab 1: Agent Skill
1. Open the `student_grades_before_fix.html` and find 4 bugs there manually. AI usage not allow in this step.

3. Now, let design our helpers. Here, we will create 3 agents to help us onboarding new project faster and smooth. 

    2.1 Documentation Agent who..
    
    2.2 Code Quality Critic Agent who..
    
    2.3 Bug Finding Agent who..

Example prompt to create agent
```
Spawn 3 sub-agent to create to create these 3 following agent skill separately. First, Documentation Agent specialize on onboarding new project it check all file in the project thoroughly and note its finding. Second, Code Quality Critic Agent who critic code quality in project. Third, bug find and fix agent who find and fix bug in the project. The skill of each agent should be created in .bob/skills/
```

5. Pausing here and think about the time we have to take talking with each agent at a time. How long you think it will take? Can we make it faster?

Find the workflow below -> 

prompt to create workflow skill
```
Create skill which is a workflow you have done in this conversation. Starting from letting the documentation and code quality agent working parallely and then pass to bugfinding agent then fix the bug`
```
