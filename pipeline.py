# main pipeline

# import a01_query as query
import a02_fetch as fetch
import a03_convert as convert
import a04_slice as window
import a05_analyze as analyze
import a06_crop as crop
import a07_extract as extract

job_id = "abc_123"
job_file_url = "https://mylam.lamresearch.com/wp-content/uploads/2018/03/cropped-cropped-lam_research_icon-32x32.png"

# got_jobs = query.main("abc", "123")
# print(got_jobs)

got_files = fetch.main(job_id, job_file_url)
print(got_files)

converted_files = convert.main(job_id)
print(converted_files)

sliced = window.main(job_id)
print(sliced)

analyzed = analyze.main("abc", "123")
print(analyzed)

cropped_values = crop.main("abc", "123")
print(cropped_values)

extracted_values = extract.main("abc", "123")
print(extracted_values)