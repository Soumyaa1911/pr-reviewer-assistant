from app.ingestion.pr_loader import get_pr_diff

diff = get_pr_diff("psf", "requests-html", pr_number=589)
print(diff[:1000])  # print first 1000 characters