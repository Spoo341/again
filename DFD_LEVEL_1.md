# DFD Level 1 - Automated Prompt Optimization System

```
                                                                                    
                    ┌─────────────────────────────────────────┐                    
                    │                                         │                    
                    │              USER                       │                    
                    │                                         │                    
                    └──────┬─────────────────────────┬────────┘                    
                           │                         │                             
                           │                         │                             
          Original Prompt  │                         │  Best Optimized Prompt      
              + Task Type  │                         │  + Improved Response        
                           │                         │  + Scores                   
                           ▼                         │                             
                    ┌─────────────┐                  │                             
                    │             │                  │                             
                    │     1.0     │                  │                             
                    │   Capture   │                  │                             
                    │    Input    │                  │                             
                    │             │                  │                             
                    └──────┬──────┘                  │                             
                           │                         │                             
                           │ Prompt + Task Type      │                             
                           ▼                         │                             
┌──────────────┐    ┌─────────────┐                 │                             
│              │◄───┤             │                 │                             
│  GEMINI API  │    │     2.0     │                 │                             
│              ├───►│  Optimize   │                 │                             
└──────────────┘    │   Prompt    │                 │                             
  Optimization      │             │                 │                             
  Request / 4       └──────┬──────┘                 │                             
  Optimized Prompts        │                        │                             
                           │ 5 Prompts              │                             
                           ▼                        │                             
┌──────────────┐    ┌─────────────┐                │                             
│              │◄───┤             │                │                             
│  GEMINI API  │    │     3.0     │                │                             
│              ├───►│  Generate   │                │                             
└──────────────┘    │  Responses  │                │                             
  5 Generation      │             │                │                             
  Requests / 5      └──────┬──────┘                │                             
  Responses                │                       │                             
                           │ 5 Prompt-Response     │                             
                           │ Pairs                 │                             
                           ▼                       │                             
                    ┌─────────────┐                │                             
                    │             │    Results     │                             
                    │     4.0     ├───────────────►│                             
                    │  Evaluate   │                │                             
                    │  Responses  │                │   ══════════════            
                    │             │◄───────────────┤   D1: Results               
                    └──────┬──────┘    Stats       │      Storage                
                           │                       │   ══════════════            
                           │ Scored Results        │                             
                           ▼                       │                             
                    ┌─────────────┐                │                             
                    │             │                │                             
                    │     5.0     ├────────────────┘                             
                    │   Display   │                                              
                    │   Results   │                                              
                    │             │                                              
                    └─────────────┘                                              
                                                                                  
                                                                                  
LEGEND:                                                                           
                                                                                  
    ┌─────────────┐                                                              
    │   Process   │  = Process (Circles in standard notation)                    
    └─────────────┘                                                              
                                                                                  
    ┌─────────────────────────┐                                                  
    │   External Entity       │  = External Entity                               
    └─────────────────────────┘                                                  
                                                                                  
    ══════════════                                                               
    Data Store                  = Data Store                                     
    ══════════════                                                               
                                                                                  
    ──────►                     = Data Flow                                      
```
