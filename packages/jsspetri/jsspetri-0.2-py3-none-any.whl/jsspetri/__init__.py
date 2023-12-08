from gymnasium.envs.registration import register

register(
     id="Jsspetri-v1",
     entry_point="jsspetri.envs.jsspetri_env:JsspetriEnv",

     nondeterministic=False,   
)




