#!/usr/bin/env R
#
# Reference: http://blog.aboutwilson.net/posts/2014-06/the-quick-and-dirty-term-structure-interpolator-in-r/
#

library(XML)
library(stringr)
library(bizdays)

str_supplant <- function (string, repl) {
    result <- str_match_all(string, "\\{([^{}]*)\\}")
    if (length(result[[1]]) == 0)
        return(string)
    result <- result[[1]]
    for (i in seq_len(dim(result)[1])) {
        x <- result[i,]
        pattern <- x[1]
        key <- x[2]
        if (!is.null(repl[[key]]))
            string <- gsub(pattern, repl[[key]], string, perl=TRUE)
    }
    string
}

.get_curve_url <- function(refdate, ticker) {
    url <- 'http://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp'
    query <- str_supplant('?Data={refdate}&Data1={sysdate}&slcTaxa={ticker}',
        list(refdate=format(as.Date(refdate), '%d/%m/%Y'),
            sysdate=format(Sys.Date(), '%Y%m%d'),
            ticker=ticker))
    paste0(url, query)
}


get_curve <- function (refdate, ticker='PRE') {
    refdate <- as.Date(refdate)
    url <- .get_curve_url(refdate, ticker)
    doc <- htmlTreeParse(url, useInternalNodes=TRUE)
    num <- xpathSApply(doc, "//td[contains(@class, 'tabelaConteudo')]",
        function(x) gsub('[\r\n \t]+', '', xmlValue(x)))
    num <- sapply(num, function(x) as.numeric(gsub(',', '.', x)), USE.NAMES=FALSE)

    colspan <- as.integer(xpathApply(doc, "//td[contains(@class, 'tabelaTitulo')]",  xmlAttrs )[[2]][3])
    if (colspan == 1) {
        terms <- num[c(TRUE, FALSE)]
        rates <- num[c(FALSE, TRUE)]/100
        log_pu <- log(1 + rates*terms/360)
        rate <- function(pu, term) (pu - 1)*(360/term)
    } else {
        terms <- bizdayse(refdate, num[c(TRUE, FALSE, FALSE)])
        rates <- num[c(FALSE, TRUE, FALSE)]/100
        log_pu <- log((1 + rates)^(terms/252))
        rate <- function(pu, term) pu^(252/term) - 1
    }

    log_price_interpolator <- approxfun(terms, log_pu, method='linear')
    function (term) {
        pu <- exp(log_price_interpolator(term))
        rate(pu, term)*100
    }
}