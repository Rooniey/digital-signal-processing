import signalGenerators as sgen

allFields = ['A', 't1', 'T', 'd', 'fp']
noise_fields = ['A', 't1', 'd', 'fp']
sin_fields = allFields

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