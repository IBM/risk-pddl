# PDDL domain inspired by risk management problem

The PDDL domain essentially describes a graph traversal from one of the designated start locations to one of the designated goal locations, with a collection of points of interest to traverse, with the aim of traversing as many as possible. The points of interest are compiled into hard goals, with a penalty paid for discarding without traversing.
The PDDL instances are generated from random graphs and thus are not representative of risk management planning problem instances tested by, e.g., [1,2].

Please cite as 

```
@InProceedings{sohrabi-et-al-aaai2018,
  author =       "Shirin Sohrabi and Anton V. Riabov and Michael Katz and Octavian Udrea",
  title =        "An {AI} Planning Solution to Scenario Generation for Enterprise Risk Management",
  booktitle =    "Proceedings of the Thirty-Second {AAAI} Conference on
                  Artificial Intelligence ({AAAI} 2018)",
  publisher =    "{AAAI} Press",
  year =         "2018",
  pages =        "160--167"
}
```


```
[1] Sohrabi, Shirin, Anton V. Riabov, Michael Katz, and Octavian Udrea. "An AI planning solution to scenario generation for enterprise risk management." In Thirty-Second AAAI Conference on Artificial Intelligence. 2018.

[2] Sohrabi, Shirin, Michael Katz, Oktie Hassanzadeh, Octavian Udrea, Mark D. Feblowitz, and Anton Riabov. "IBM scenario planning advisor: plan recognition as AI planning in practice." AI Communications 32, no. 1 (2019): 1-13.
```