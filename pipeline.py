# main pipeline

# import a01_query as query
import a02_fetch as fetch
import a03_convert as convert
import a04_slice as window
import a05_analyze as analyze
import a06_crop as crop
import a07_extract as extract

# job_id = "abc_123"
# job_file_url = "https://mylam.lamresearch.com/wp-content/uploads/2018/03/cropped-cropped-lam_research_icon-32x32.png"
# job_file_url = "https://www.arcat.com/cad/zurnind/221316_z9a-fd4.pdf"

job_id = "bcd_234"
job_file_url = "https://ed.iitm.ac.in/~raman/Autodesk%20Inventor%20Practice%20Part%20Drawings.pdf"

# got_jobs = query.main("abc", "123")
# print(got_jobs)

job_path = fetch.main(job_id, job_file_url)
print(job_path)

converted_files_dir = convert.main(job_id, job_path)
print(converted_files_dir)

sliced = window.main(job_id, job_path)
print(sliced)

analyzed = analyze.main(job_id, job_path)
print(analyzed)

cropped_values = crop.main(job_id, job_path)
print(cropped_values)

extracted_values = extract.main(job_id, job_path)
print(extracted_values)