import bibtexparser

def parse_bibtex(file_path):
    with open(file_path, 'r', encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    return bib_database.entries

def group_by_keywords(entries):
    keyword_groups = {}
    for entry in entries:
        if 'keywords' in entry:
            keywords = entry['keywords'].split(', ')
            main_keyword = keywords[0]
            sub_keyword = keywords[1] if len(keywords) > 1 else None

            if main_keyword not in keyword_groups:
                keyword_groups[main_keyword] = {}
            if sub_keyword:
                if sub_keyword not in keyword_groups[main_keyword]:
                    keyword_groups[main_keyword][sub_keyword] = []
                keyword_groups[main_keyword][sub_keyword].append(entry)
            else:
                if None not in keyword_groups[main_keyword]:
                    keyword_groups[main_keyword][None] = []
                keyword_groups[main_keyword][None].append(entry)

    return keyword_groups

def generate_mindmap(keyword_groups):
    mindmap = "\\begin{tikzpicture}[mindmap, grow cyclic, every node/.style=concept, concept color=orange!40,\n"
    mindmap += "\tlevel 1/.append style={level distance=5cm,sibling angle=90},\n"
    mindmap += "\tlevel 2/.append style={level distance=4cm,sibling angle=45},]\n"
    mindmap += "\\path[mindmap,concept color=black,text=white]\n"
    mindmap += "\\node{Foundation Models for LLMs in Programming}\n"

    for main_keyword, sub_keyword_groups in keyword_groups.items():
        mindmap += f"child {{ node {{{main_keyword.capitalize()}}}\n"

        for sub_keyword, entries in sub_keyword_groups.items():
            if sub_keyword:
                mindmap += f"\tchild {{ node {{{sub_keyword.capitalize()}}}\n"

            for entry in entries:
                title = entry['title']
                mindmap += f"\tchild {{ node {{{title}}} }}\n"

            if sub_keyword:
                mindmap += "}\n"

        mindmap += "}\n"

    mindmap += ";\n"
    mindmap += "\\end{tikzpicture}"
    return mindmap

def save_mindmap_to_file(mindmap, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(mindmap)

def main():
    bibtex_file = 'bibtex.bib'
    output_file = 'mindmap.tex'

    entries = parse_bibtex(bibtex_file)
    keyword_groups = group_by_keywords(entries)
    mindmap = generate_mindmap(keyword_groups)

    save_mindmap_to_file(mindmap, output_file)
    print(f"Mindmap generated and saved to {output_file}")

if __name__ == '__main__':
    main()