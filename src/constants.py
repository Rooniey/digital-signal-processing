import signalGenerators as sgen

noise_fields = ['n', 'A', 't1', 'd']
sin_fields = ['A', 't1', 'T', 'd', 'n']

signals={
    'uniform_noise': {
        'fn': sgen.uniform_noise,
        'fields': noise_fields,
    },
    'gaussian_noise': {
        'fn': sgen.gaussian_noise,
        'fields': noise_fields,
    },
    'sin': {
        'fn': sgen.sin,
        'fields': sin_fields,
    },
}