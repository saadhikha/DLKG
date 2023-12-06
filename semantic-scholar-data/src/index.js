import fetch from "node-fetch"
import { appendFileSync, writeFileSync, readFileSync } from "fs"

const API_KEY = "woZhcbJHSS582OzTD5l952d7xMZwJO3P7FSgNlel"
const MAX_RETRIES = 3
const BASE_URL = "https://api.semanticscholar.org"
const MAX_PAPER_COUNT = 1000000
const MIN_CITATION_COUNT = 50
const BASE_HEADERS = {
  'Content-Type': 'application/json',
  'x-api-key': API_KEY
}
const CSV_FILE = 'data-final-2.csv'
let totalPaperCount = 0
const paperIds = new Set()

/**
 * read csv file using readFileSync and get all paper ids
 */
function readExistingDataset() {
  const csv = readFileSync('okdata.csv', 'utf-8');
  const lines = csv.split('\n');
  for (const line of lines) {
    const paperId = line.split(',')[0];
    if (paperId) paperIds.add(paperId);
  }
  return paperIds;
}
readExistingDataset()
console.log(paperIds)

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
        console.log(`Retrying... Attempt number ${retryCount + 1}, `, `${error}`);
        return await retryingFetchInternal(retryCount + 1);
      } else {
        console.error(`Fetch error of: ${url}`, error);
      }
    }
  }

  return await retryingFetchInternal()
}

async function fetchPaper(paperId, fields=null) {
  fields = fields ?? ["url", "year", "title", "authors", "s2FieldsOfStudy", "venue"]
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
      data.venue,
      quoteScope(data.fieldsOfStudy.join(',')),
      quoteScope(data.authors.join(',')),
      quoteScope(data.citations.join(','))
  ].join(',') + '\n';
  appendFileSync(CSV_FILE, csvLine);
  console.success(`Paper [${data.title}] written to CSV`)
}

async function buildDatasetWithPaper(entryPaperId) {
  const paper = await fetchPaper(entryPaperId)
  if (!paper || !paper.paperId) return
  const paperData = {
    paperId: paper.paperId,
    title: paper.title.replace(/\n/g, ' ').replace(/"/g, "'"),
    year: paper.year,
    venue: paper.venue,
    fieldsOfStudy: [...new Set(paper.s2FieldsOfStudy.map(field => field.category))],
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
    writeFileSync(CSV_FILE, 'paperId,title,year,fieldsOfStudy,authors,citations\n');
  }
  await buildDatasetWithPaper(entryPaperId)
}

// resnet
buildDataset("b5c26ab8767d046cb6e32d959fdf726aee89bb62")

// bert
buildDataset("df2b0e26d0599ce3e70df8a9da02e51594e0e992")

// fast rcnn
buildDataset("424561d8585ff8ebce7d5d07de8dbf7aae5e7270")

// nerf
buildDataset("428b663772dba998f5dc6a24488fff1858a0899f")

// unet
buildDataset("6364fdaa0a0eccd823a779fcdd489173f938e91a")

// transformer
buildDataset("204e3073870fae3d05bcbc2f6a8e263d9b72e776")

// gpt
buildDataset("cd18800a0fe0b668a1cc19f2ec95b5003d0a5035")

// rl
buildDataset("aee6d6b3282662b69a1020c95be725e0075428bd")
