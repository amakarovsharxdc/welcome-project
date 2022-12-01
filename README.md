# Welcome-project. Homework for Software Engineer

**Hi there!**

We want to check your basic skills and want you show us how you're cool!

It will help us save your time to not ask dumb questions.

We suppose you will show us how do you:

- Write and organize code
- Unit test
- Doc your code/solution

We understand and don't require you spend a lot of time on that task, so just:

1. Write algorithm
2. 2-3 unit tests
3. Few lines of docs explaining your solution and how to use it

Below you can find problem you need to solve.

`Please fork this repo and solve the problem and send us PR to review.`

`If you need clarification or have question about problem input - it's ok, just create issue `


**Good luck and see you later!**

## Problem

We want to get common/library solution for all developers in our company.

We have 2 and more service's API and want to build map structure built from these data.


### Examples of input data

Each service has array of tuples (verb, path). 


                 verb           path
                  |              |
                  |              |

    service1 = [("GET", "/api/v1/cluster/metrics"),
                ("POST", "/api/v1/cluster/{cluster}/plugins"),
                ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}")]


    service2 = [("GET", "/api/v1/cluster/freenodes/list"),
                ("GET", "/api/v1/cluster/nodes"),
                ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}"),
                ("POST", "/api/v1/cluster/{cluster}/plugins")]


Words in braces '{}' are parameters


### Solution

Design, test and doc module/s what implement logic


*Scenario 1*. First call


    IN ->    [("GET", "/api/v1/cluster/metrics"),
              ("POST", "/api/v1/cluster/{cluster}/plugins"),
              ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}")]

                                |

    LOGIC ->            parse and collect data
                        
        1. build map by splitting "/" path without version (/api/v1) and without parameters ({cluster})
        2. map looks like tree where leaf is verb (method - POST, GET)

                                |

    OUT ->      {'cluster': 
                    {'metrics': 'GET', 
                    'plugins': 'POST'}
                }    


*Scenario 2*. Second call with another data


    IN ->    [("GET", "/api/v1/cluster/freenodes/list"),
              ("GET", "/api/v1/cluster/nodes"),
              ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}"),
              ("POST", "/api/v1/cluster/{cluster}/plugins")]

                                |

    LOGIC ->            parse and collect data
                        
        1. priosly data exists
        2. if path/sub tree doesn't exists - create
        3. if path/sub tree exists - check verb
            3.1 if verb is same - just skip 
            3.2 if verb is different - raise Exception with full path to verb 

                                |

    OUT ->     {'cluster': 
                    {'metrics': 'GET', 
                    'plugins': 'POST', 
                    'freenodes': {'list': 'GET'}, 
                    'nodes': 'GET'
                    }
                }


### Limitations

- We cannot get that data on same time, so you need to store data in memory and update it after each next request.
    
                                        (library)
        service1  ---------->      JSON (create if not exists)
                    send data

        service2  ---------->      JSON  (update existing data)
                    send data


- service1 and service2 may have same API/data - tuple (verb, path) 


