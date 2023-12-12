import asta

path = 'test_data.csv'
p, _, _ = asta.full_algorithm(file_path=path,
                              cutoff_value=2.0,
                              should_save_plot=True)
print(p)