1. search_file_by_codon.py ищет стоп-кодоны внутри всех генов с отступом от концов 5%.
На входе: direct - папка со всеми генами (/mnt/lustre/potapova/200_flies/all_genes/).
На выходе: files_with_stop_codon.txt - записывает названия файлов с найденными стоп-кодонами в один файл.

2. search_file_by_codon_wo_remove.py ищет стоп-кодоны внутри всех генов без отступа от концов.
Старая версия скрипта search_file_by_codon.py.
На входе: direct - папка со всеми генами (/mnt/lustre/potapova/200_flies/all_genes/).
На выходе: files_with_stop_codon.txt - записывает названия файлов с найденными стоп-кодонами в один файл.

3. create_list_files_wo_stop.py записывает список файлов, которые не содержат отобранные стоп-кодоны.
На входе: direct - папка со всеми генами (/mnt/lustre/potapova/200_flies/all_genes/);
        files_with_stop_codon.txt - файл с названими файлов с найденными стоп-кодонами.
На выходе: files_wo_stop_codons.txt - записывает названия файлов без стоп-кодонов, указанных в files_with_stop_codon.txt, в один файл.

4. counting_frequency_stop_in_gene_by_threshold.py создает файлы, в которых посчитана частота стоп-кодонов, и отбирает те, которые проходят пороговую частоту.
На входе: direct - папка со всеми генами (/mnt/lustre/potapova/200_flies/all_genes/);
        files_with_stop_codon.txt - названия файлов с найденными стоп-кодонами.
На выходе: all_genes_with_stop.txt - файл со всеми генами всех организмов с указанием стоп-кодонов и их частот в гене.
        threshold_genes_with_stop - создает набор файлов с генами, которые имеют частоту стоп-кодона ниже пороговой.
        no_threshold_genes_with_stop - создает набор файлом с названиями файлов, кгены в которых не прошли порог частоты стоп-кодонов.

5. counting_frequency_pairs_genes_by_threshold.py
Параметры: a[0] - threshold, a[1] - number_neighbors.
На входе: threshold_genes_with_stop (результат работы counting_frequency_stop_in_gene_by_threshold.py)
        files_wo_stop_codons.txt (результат работы create_list_files_wo_stop.py)
        no_threshold_genes_with_stop (результат работы counting_frequency_stop_in_gene_by_threshold.py)
На выходе:
        description_pairs_genes - файл с названиями файлов пары генов, id организма, в котором встречаются обы стоп-кодона, позиция стоп-кодона и его буквенное обозначение в этих генах.
        frequency_pairs_genes - файл с названиями файлов пары генов и с их частотой встречаемости стоп-кодонов в одном организме (p_ab). Нет нулевых частот.

6. negative_control.py - тот же смысл, что и у counting_frequency_pairs_genes_by_threshold.py, только для генов, которые находятся на разных хромосомах. Гены образуют пары попорядку.
Параметры: a[0] - threshold, a[1] - number_neighbors.
На входе: threshold_genes_with_stop (результат работы counting_frequency_stop_in_gene_by_threshold.py)
        files_wo_stop_codons.txt (результат работы create_list_files_wo_stop.py)
        no_threshold_genes_with_stop (результат работы counting_frequency_stop_in_gene_by_threshold.py)
На выходе:
        description_pairs_genes - файл с названиями файлов пары генов, id организма, в котором встречаются обы стоп-кодона, позиция стоп-кодона и его буквенное обозначение в этих генах.
        frequency_pairs_genes - файл с названиями файлов пары генов и с их частотой встречаемости стоп-кодонов в одном организме (p_ab). Нет нулевых частот.

negative_control_more_pairs.py - тот же смысл, что и у counting_frequency_pairs_genes_by_threshold.py, только для генов, которые находятся на разных хромосомах. Берется заданное количестсво пар между генами (например, все попарные комбинации первых 50 генов с разных хромосом и так далее по всей длине хромосом).
Параметры: a[0] - threshold, a[1] - number_neighbors.
На входе: threshold_genes_with_stop (результат работы counting_frequency_stop_in_gene_by_threshold.py)
        files_wo_stop_codons.txt (результат работы create_list_files_wo_stop.py)
        no_threshold_genes_with_stop (результат работы counting_frequency_stop_in_gene_by_threshold.py)
На выходе:
        description_pairs_genes - файл с названиями файлов пары генов, id организма, в котором встречаются обы стоп-кодона, позиция стоп-кодона и его буквенное обозначение в этих генах.
        frequency_pairs_genes - файл с названиями файлов пары генов и с их частотой встречаемости стоп-кодонов в одном организме (p_ab). Нет нулевых частот.

7. counting_frequency_pairs_genes.py (старый файл). Не передаются параметры.
На входе: threshold_genes_with_stop (результат работы counting_frequency_stop_in_gene_by_threshold.py)
        files_wo_stop_codons.txt (результат работы create_list_files_wo_stop.py)
На выходе (имена другие, надо исправить):
        description_pairs_genes - файл с названиями файлов пары генов, id организма, в котором встречаются обы стоп-кодона, позиция стоп-кодона и его буквенное обозначение в этих генах.
        frequency_pairs_genes - файл с названиями файлов пары генов и с их частотой встречаемости стоп-кодонов в одном организме (p_ab). Нет нулевых частот.

8. frequency_b_in_a.py
Параметры: a[0] - threshold, a[1] - number_neighbors (на Макарыче)
На входе: frequency_pairs_genes (результат работы counting_frequency_pairs_genes_by_threshold.py)
        threshold_genes_with_stop (результат работы counting_frequency_stop_in_gene_by_threshold.py)
На выходе: frequency_b_in_a_max_a - файл со списком пар генов и частотами frequency_max_a, frequency_min_b, frequency_ab, frequency_b_in_a

9. LD.py
Параметры: a[0] - threshold
На входе: frequency_pairs_genes (результат работы counting_frequency_pairs_genes_by_threshold.py)
        threshold_genes_with_stop (результат работы counting_frequency_stop_in_gene_by_threshold.py)
На выходе: LD - файл со списком пар генов и значением LD и r2

10. frequency_n.py - считает число N на месте всех стоп-кодонов по всему гену в других организмах.
На входе: direct - папка со всеми генами (/mnt/lustre/potapova/200_flies/all_genes/).
На выходе:
        stop_codon_relative_coordinate.txt - файл с данными в формате json с информацией о стоп-кодонах
            внутри генов без отрезанных 5% гена с обоих сторон (координата, стоп-кодон, имя файла, id).
        list_stop_codon_before.txt - список файлов, в которых есть стоп-кодоны.
        list_stop_codon_after.txt - список файлов, в которых есть стоп-кодоны без N в других организмах.

11. search_frameshift.py - смотрит на длину строк (генов) в одном файле, и если она разная, то записывает имя файла в создаваеммый файл.
На входе: direct - папка со всеми генами (/mnt/lustre/potapova/200_flies/all_genes/).
На выходе:
        files_with_frameshift.txt - файл со списком названий файлов, в которых гены неодинаковой длины.

