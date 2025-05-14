# Vacancy Search and Analysis Tool

This tool allows you to search for vacancies, filter them based on keywords and salary range, sort them, and view the top results. It is designed to help users quickly find relevant job opportunities based on their preferences.

## Getting Started

### Prerequisites

-   **Python 3.12**: Ensure you have Python 3.12 installed.
-   **Dependencies**: The project requires several Python packages. Install them using:
  pip install -r requirements.txt

## Project Functionalities

This project is a Vacancy Search and Analysis Tool designed to help users find relevant job opportunities quickly and efficiently. It connects to an external job search API, retrieves vacancy data, and provides a variety of tools for filtering, sorting, and ranking these vacancies based on user preferences.

The tool provides the following key functionalities:

1.  **Vacancy Search:**
    *   **API Interaction:** The tool connects to an external job search API (e.g., HeadHunter) to retrieve job vacancy data.
    *   **User Query:** Users can input a search query to specify the type of job vacancies they are looking for.

2.  **Data Handling:**
    * **Data Storage**: The data fetched from the API can be saved to a file to be used later.

3.  **User-Defined Filtering:**
    *   **Keyword Filtering:** Users can input specific keywords to filter vacancies based on their skills, interests, or required technologies.
    *   **Salary Range Filtering:** Users can define a salary range (e.g., "1000-2000") to narrow down the search results to vacancies that meet their desired compensation.

4.  **Sorting and Ranking:**
    *   **Salary-Based Sorting:** The tool sorts the filtered vacancies by salary in descending order, allowing users to easily identify the highest-paying opportunities.
    *   **Top N Ranking:** The tool can rank and display the top N vacancies based on the user's defined criteria and the provided salary range.

5.  **User Interaction:**
    *   **Command-Line Interface (CLI):** The tool provides a user-friendly command-line interface.
    *   **Interactive Prompts:** The CLI guides users through the process of entering search queries, filtering keywords, and salary ranges.
    *   **Organized Output:** The results are displayed in an organized and readable format in the command line, allowing users to easily review the list of relevant vacancies.

In essence, this tool is designed to streamline the job search process by automating the retrieval, filtering, sorting, and ranking of job vacancies according to user-defined criteria.

