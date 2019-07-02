# Metadata

- Performance:

    - Tot time: 24737.7256
    - Time preprocessing: 0.0004
    - Time for processing: 24737.7252
        - of which 1009.0553 is overhead

- Environment:

    - Clean up caches every iteration
    - Freqency 1.5 GHz
    - Turbo off
    - no cpu isolate
    - no taskset
    
- Result test:

    - [ 2mm ] p-value: 0.0 IID: False
    - [ bicg ] p-value: 0.0006419154 IID: False
    - [ correlation ] p-value: 0.0017521098 IID: False
    - [ floyd-warshall ] p-value: 0.0267720007 IID: False
    - [ lu ] p-value: 1.02545e-05 IID: False
    - [ trisolv ] p-value: 0.0007845673 IID: False