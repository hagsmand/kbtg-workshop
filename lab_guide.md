# Bob Workshop

## 0. Setup
1. Download installer from [https://bob.ibm.com/download](https://bob.ibm.com/download)

2. Install Bob and try log in

## Lab 1: Agent Skill
1. Open the `student_grades_before_fix.html` and find 4 bugs there manually. AI usage not allow in this step.

3. Now, let design our helpers. Here, we will create 4 modes to help us onboarding new project faster and smooth. 

    2.1 Documentation Agent who..
    
    2.2 Code Quality Critic Agent who..
    
    2.3 Bug Finding Agent who..

Example prompt to create mode
```
Create Documentation Agent specialize on onboarding new project. Check all file in the project thoroughly and note its finding. The mode file should be created in .bob/custom_modes.yaml
```

5. Pausing here and think about the time we have to take talking with each agent at a time. How long you think it will take? Can we make it faster?

Find the workflow below -> 

Example prompt to run Documentation Agennt and Code Quality Critic agent parallely
```
Let the Documentation Agent and Code Quality Critic Agent onboarding this project parallely.
```

Now, run prompt to let the Bug Finding Agent work after those 2
```
Let the bug finding agent work after the finding of these 2 agents
```

Lastly, prompt to create workflow skill
```
Create skill which is a workflow you have done in this conversation. Starting from letting the documentation and code quality agent working parallely and then pass to bugfinding agent then fix the bug`
```
