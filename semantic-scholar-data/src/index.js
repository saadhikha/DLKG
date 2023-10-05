import fetch from "node-fetch"
import { appendFileSync, writeFileSync } from "fs"

const API_KEY = "woZhcbJHSS582OzTD5l952d7xMZwJO3P7FSgNlel"
const MAX_RETRIES = 3
const BASE_URL = "https://api.semanticscholar.org"
const MAX_PAPER_COUNT = 5000
const MIN_CITATION_COUNT = 50
const BASE_HEADERS = {
  'Content-Type': 'application/json',
  'x-api-key': API_KEY
}
const CSV_FILE = 'data.csv'
let totalPaperCount = 0
const paperIds = new Set()

async function retryingFetch(url, options) {
  url = `${BASE_URL}/${url}`
  async function retryingFetchInternal(retryCount=0) {
    try {
      console.log(`Fetching: ${url}`)
      const response = await fetch(url, { headers: BASE_HEADERS, ...options })
      const data = await response.json()
      return data
    } catch (error) {
      if (retryCount < MAX_RETRIES) {
        console.log(`Retrying... Attempt number ${retryCount + 1}`);
        return await retryingFetchInternal(retryCount + 1);
      } else {
        console.error(`Fetch error of: ${url}`, error);
      }
    }
  }

  return await retryingFetchInternal()
}

async function fetchPaper(paperId, fields=null) {
  fields = fields ?? ["url", "year", "title", "authors"]
  return await retryingFetch(`graph/v1/paper/${paperId}?fields=${fields.join(",")}`)
}

async function fetchPaperCitations(paperId, offset=0, fields=null) {
  fields = fields ?? ["citationCount"]
  const limit = offset === 9000 ? 999 : 1000
  return await retryingFetch(`graph/v1/paper/${paperId}/citations?fields=${fields.join(",")}&offset=${offset}&limit=${limit}`)
}

async function getValidCitations(paperId) {
  const allCitations = []
  let offset = 0
  while (offset !== null && offset < 9000) {
    const citations = await fetchPaperCitations(paperId, offset)
    offset = citations.next
    for (const { citingPaper } of citations.data ?? []) {
      if (paperIds.has(citingPaper.paperId)) continue
      if (citingPaper.citationCount <= MIN_CITATION_COUNT) continue
      allCitations.push(citingPaper.paperId)
    }
  }

  return allCitations
}


function quoteScope(str) {
  return `"${str}"`
}

console.success = function (msg) {
  console.log('\x1b[32m%s\x1b[0m', msg);
}

function writePaperToCsv(data) {
  const csvLine = [
      data.paperId,
      quoteScope(data.title),
      data.year,
      quoteScope(data.authors.join(',')),
      quoteScope(data.citations.join(','))
  ].join(',') + '\n';
  appendFileSync(CSV_FILE, csvLine);
  console.success(`Paper [${data.title}] written to CSV`)
}

async function buildDatasetWithPaper(entryPaperId) {
  const paper = await fetchPaper(entryPaperId)
  if (!paper) return
  const paperData = {
    paperId: paper.paperId,
    title: paper.title,
    year: paper.year,
    authors: paper.authors?.map(author => author.name) ?? [],
    citations: await getValidCitations(entryPaperId)
  }
  writePaperToCsv(paperData)
  paperIds.add(paperData.paperId)
  totalPaperCount += 1
  for (const citation of paperData.citations) {
    if (totalPaperCount >= MAX_PAPER_COUNT) return
    await buildDatasetWithPaper(citation)
  }
}
async function buildDataset(entryPaperId, resume=false) {
  if (!resume) {
    writeFileSync(CSV_FILE, 'paperId,title,year,authors,citations\n');
  }
  await buildDatasetWithPaper(entryPaperId)
}

// resnet
let pid = "b5c26ab8767d046cb6e32d959fdf726aee89bb62"

// pid = "3813b88a4ec3c63919df47e9694b577f4691f7e5"

// pid = "3a906b77fa218adc171fecb28bb81c24c14dcc7b"

buildDataset(pid)
