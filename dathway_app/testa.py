import re

def extract_tech_skills(bot_response):
    # Match lines starting with numbers, extract skills and compatibility ratings
    pattern = r'(\d+\.\s\*\*(.*?)\*\*.+?Compatibility: (\d+)/10)'
    matches = re.findall(pattern, bot_response)

    skills_list = [{'skill': match[1], 'compatibility': int(match[2])} for match in matches]

    return skills_list

# Example usage:
bot_response = """
Great! Here are 5 tech skills that you might find interesting, rated based on compatibility with your socio-activities and academic background:
1. Sports Analytics - Utilizing data and mathematical models for sports performance analysis and strategy. (Compatibility: 9/10)
2. Data Science with Python - Applying mathematical concepts to analyze and interpret sports data. (Compatibility: 8/10)
3. Mobile App Development for Fitness - Creating mobile apps for fitness tracking and sports-related activities. (Compatibility: 7/10)
4. Statistical Modeling with R - Using statistical techniques in sports data analysis. (Compatibility: 8/10)
5. Game Development with Unity - Building football-themed games or interactive experiences. (Compatibility: 6/10)
Please keep in mind that these suggestions are based on the information provided. Feel free to explore them further and see which ones resonate with you the most.
"""

skills = extract_tech_skills(bot_response)
print(skills)
