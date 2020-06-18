from schema import Schema, And, Or, Use, Optional, Regex

DATE_ISO = "^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])(T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$)*"
URL_FORMAT = "^http(s)*://"
CONTEXT = "https://schema.org(/)*"

organization_schema = Schema({
    "@context": Regex(CONTEXT),
    "@type": Or("Corporation","Organization"),
    "name": str,
    Optional("alternateName"): str,
    Optional("url"): Regex(URL_FORMAT),
    Optional("logo"): Regex(URL_FORMAT),
    Optional("sameAs"): Or(str, [str]),
    Optional(str): object
})

person_schema = Schema({
    "@context": Regex(CONTEXT),
    "@type": "Person",
    "name": str,
    Optional("url"): Regex(URL_FORMAT),
    Optional("image"): Regex(URL_FORMAT),
    Optional("sameAs"): Or(Regex(URL_FORMAT), [Regex(URL_FORMAT)]),
    Optional("jobTitle"): str,
    Optional("worksFor"):{
        "@type": "Organization",
        "name": str
    },
    Optional(str): object
})

article_schema = Schema({
    "@context": Regex(CONTEXT),
    "@type": Or("Article", "BlogPosting", "NewsArticle"),
    Optional("mainEntityOfPage"): {
        "@type": "WebPage",
        "@id" : str
    },
    "headline": str,
    "image": Or(Regex(URL_FORMAT),[Regex(URL_FORMAT)]),
    "author": {
        "@type": And(str, lambda s: s in ("Person", "Organization")),
        "name": str
    },
    "publisher": {
        "@type": "Organization",
        "name": str,
        Optional("logo"):{
            "@type": "ImageObject",
            "url": Regex(URL_FORMAT),
            Optional("width"): Or(int, float),
            Optional("height"): Or(int, float)
        }
    },
    "datePublished": Regex(DATE_ISO),
    Optional("dateModified"): Regex(DATE_ISO),
    Optional(str): object
})

breadcrumb_schema = Schema({
    "@context": Regex(CONTEXT),
    "@type": "BreadcrumbList",
    "itemListElement": [{
        "@type": "ListItem",
        "position": int,
        "name": str,
        "item": Regex(URL_FORMAT)
    }],
    Optional(str): object
})

faq_schema = Schema({
    "@context": Regex(CONTEXT),
    "@type": "FAQPage",
    "mainEntity": [{
        "@type": "Question",
        "name": str,
        "acceptedAnswer": {
            "@type": "Answer",
            "text": str
        }
    }]
})

video_schema = Schema({
    "@context": Regex(CONTEXT),
    "@type": "VideoObject",
    "name": str,
    "description": str,
    "thumbnailUrl": Or(Regex(URL_FORMAT), [Regex(URL_FORMAT)]),
    "uploadDate": Regex(DATE_ISO),
    Optional("contentUrl"): Regex(URL_FORMAT),
    Optional("embedUrl"): Regex(URL_FORMAT),
    Optional("publisher"):{
        "@type": "Organization",
        "name": str,
        Optional("logo"):{
            "@type": "ImageObject",
            "url": Regex(URL_FORMAT),
            Optional("width"): Or(int, float),
            Optional("height"): Or(int, float)
        }
    },
    Optional(str): object
})

review_schema = {
        "@type": "Review",
        Optional("name"): str,
        Optional("reviewBody"): str,
        "reviewRating": {
            "@type": "Rating",
            "ratingValue": str,
            "bestRating": str,
            "worstRating": str,
        },
        "datePublished": Regex(DATE_ISO),
        "author":{
            "@type": "Person",
            "name": str,
        },
        Optional("publisher"):{
            "@type": "Organization",
            "name": str
        },
        Optional(str): object
}

product_schema = Schema({
    "@context": Regex(CONTEXT),
    "@type": "Product",
    "name": str,
    "image": Or(Regex(URL_FORMAT), [Regex(URL_FORMAT)]),
    Optional("description"): str,
    Optional("sku"): str,
    Optional("mpn"): str,
    Optional("brand"): Or(str, {
            "@type": "Brand",
            "name": str
        }),
    Optional("review"): Or(review_schema,[review_schema]),
    Optional("aggregateRating"): {
        "@type": "aggregateRating",
        "ratingValue": str,
        "reviewCount": str,
        "bestRating": str,
        "worstRating": str
    },
    Optional("Offers"):{
        "@type": "Offer",
        "url": Regex(URL_FORMAT),
        "priceCurrency": str,
        "price": str,
        "priceValidUntil": Regex(DATE_ISO),
        "availability": Regex(URL_FORMAT),
        "itemCondition": Regex(URL_FORMAT),
        Optional("seller"): {
            "@type": "Organization",
            "name": str
        }
    },
    Optional(str): object
})

all_schemas = {
    "Organization": organization_schema,
    "Corporation": organization_schema,
    "Person": person_schema,
    "Article": article_schema,
    "BlogPosting": article_schema,
    "NewsArticle": article_schema,
    "BreadcrumbList": breadcrumb_schema,
    "FAQPage": faq_schema,
    "VideoObject": video_schema,
    "Product": product_schema
}