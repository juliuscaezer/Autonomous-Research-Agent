function ResultCard({ url, summary }) {
  return (
    <div className="result-card">
      <a href={url} target="_blank" rel="noopener noreferrer">
        <h3>{url}</h3>
      </a>
      <p>{summary}</p>
    </div>
  )
}

export default ResultCard
