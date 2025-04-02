import streamlit as st
from db import db_client
from rai import rai_client
import json

def main():
    st.title("🤖 Relevance AI Labs 3")
    
    tab1, tab2, tab3 = st.tabs(["Run Agent", "Run Tool", "View Outputs"])
    
    # Run Agent
    with tab1:
        with st.form("meeting_prep_form"):
            name = st.text_input("Name", placeholder="Enter person's name")
            company = st.text_input("Company", placeholder="Enter company name")
            submit = st.form_submit_button("Research")
            
        if submit:
            message = f"""
            Research the following person for my meeting:
            {name}
            Company: {company}
            """
            
            with st.spinner("Researching..."):
                agent_id = "4889a5ae-7512-447f-8122-368be3a01a01" # meeting agent
                task_output = rai_client.trigger_agent(message=message, agent_id=agent_id)
                
                if task_output:
                    with st.container(border=True):
                        st.write("### Research Results")
                        st.write(task_output["answer"])
                    
                    try:
                        data = {
                            "name": name,
                            "company": company,
                            "notes": task_output["answer"]
                        }
                        
                        db_client.create(data, "agent_outputs")
                        
                        st.success("Successfully saved to Airtable!")
                    except Exception as e:
                        st.error(f"Failed to save to Airtable: {str(e)}")
    
    # Run Tool
    with tab2:
        with st.form("search_form"):
            search_query = st.text_input("Search Query", placeholder="Enter search term")
            search_submit = st.form_submit_button("Search")
            
        if search_submit:
            with st.spinner("Searching..."):

                tool_id = "600da11f-eba1-47cf-8d77-ed4f86fd48dd"  # Google Search Tool
                tool_output = rai_client.trigger_tool(
                    tool_id=tool_id, 
                    params={"search_query": search_query}
                )
                
                if tool_output:
                    with st.container(border=True):
                        st.write("### Search Results")
                        search_results = tool_output.output["answer"]["organic"]
                        
                        for result in search_results:
                            with st.container(border=True):
                                st.markdown(f"**[{result['title']}]({result['link']})**")
                                st.write(result['snippet'])
                                if 'date' in result:
                                    st.caption(f"Date: {result['date']}")
                                st.caption(f"Position: {result['position']}")
                            st.divider()
                        
                        try:
                            data = {
                                "query": search_query,
                                "results": json.dumps(search_results) 
                            }
                            
                            db_client.create(data, "tool_outputs")
                            
                            st.success("Successfully saved to Airtable!")
                        except Exception as e:
                            st.error(f"Failed to save to Airtable: {str(e)}")
        
    # View Outputs             
    with tab3:
        with st.form("view_outputs_form"):
            table_choice = st.selectbox(
                "Select Table",
                options=["agent_outputs", "tool_outputs"],
                key="table_selector"
            )
            refresh_submit = st.form_submit_button("Refresh Data")
        
        if refresh_submit:
            with st.spinner("Loading records..."):
                records = db_client.read_all(table_choice)
                
                table_data = [record['fields'] for record in records]
                
                if table_data:
                    st.table(table_data)
                else:
                    st.info("No records found")

if __name__ == '__main__':
    main()