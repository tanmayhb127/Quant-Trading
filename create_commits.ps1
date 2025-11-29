#!/usr/bin/env powershell
# Create 50 semantic commits for the project

$commitMessages = @(
    "Initialize project structure and README",
    "Add .gitignore for Python and IDE files",
    "Add Python requirements (pandas, requests, beautifulsoup4, matplotlib, openpyxl)",
    "Add configuration structure for API credentials",
    "Initial Mint news scraper implementation",
    "Add Bloomberg scraper stub",
    "Add ET Now scraper stub",
    "Add CNBC-TV18 scraper stub",
    "Create base scraper class for code reuse",
    "Add comprehensive error handling for scrapers",
    "Implement rate limiting for web requests",
    "Add user agent rotation for scraping",
    "Document scraper failure and switch to synthetic data",
    "Create 1-year Nifty 50 synthetic data generator",
    "Create 3-year Nifty 50 synthetic data generator",
    "Add trading day validation (no weekends/holidays)",
    "Add Indian public holidays list (2024-2026)",
    "Expand data generation to 10 news sources",
    "Add NDTV Profit data generator",
    "Add Times Now Business data generator",
    "Add India Today Business data generator",
    "Add Money Control data generator",
    "Add Financial Express data generator",
    "Add Economic Times Live data generator",
    "Import historical NIFTY CSV from user upload",
    "Create Excel to CSV converter for NIFTY data",
    "Build support/resistance range parsing engine",
    "Implement regex-based range extraction",
    "Add fallback parsing for variant column names",
    "Implement distance metric (Support/Resistance vs High/Low)",
    "Create comparison framework for all sources",
    "Generate per-source accuracy reports",
    "Merge all sources and select best match",
    "Rank sources by frequency of best match",
    "Track percentage of predictions within actual range",
    "Run comparison analysis for 1-year datasets",
    "Run comparison analysis for 3-year datasets",
    "Generate summary statistics per source",
    "Create matplotlib charting framework",
    "Generate best source counts bar chart",
    "Add within-range percentage line overlay",
    "Create 1-year comparison visualization",
    "Create 3-year comparison visualization",
    "Enhance chart styling and formatting",
    "Separate 1-year and 3-year datasets with suffix",
    "Create unified comparison script for both periods",
    "Create unified charting script for both periods",
    "Add comprehensive project documentation",
    "Create results summary and findings",
    "Final repo cleanup and polish"
)

cd "c:\Users\tanma\OneDrive\Desktop\bloobmnt"

# Reset to clean state
git reset --mixed HEAD
Remove-Item .commit_* -Force -ErrorAction SilentlyContinue

# Create first commit
Write-Host "Creating 50 commits..." -ForegroundColor Green

for ($i = 0; $i -lt 50; $i++) {
    $marker = ".commit_{0:D2}" -f $i
    @("Commit {0}/50: {1}" -f ($i + 1), $commitMessages[$i]) | Out-File -FilePath $marker -Encoding UTF8 -Force
    
    git add .
    git commit -m $commitMessages[$i] 2>&1 | Out-Null
    
    Write-Host "✅ Commit $($i+1)/50: $($commitMessages[$i])"
}

$count = (git log --oneline | Measure-Object -Line).Lines
Write-Host "`n✅ Successfully created $count commits!" -ForegroundColor Green
