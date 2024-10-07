# LAB PAGE
if selected == 'Lab':

    st.markdown(f"<h2 style='text-align: center; padding: 10'>Data Analysis</h2>", unsafe_allow_html=True)           
    st.markdown(f"""
                <p style='text-align: center; padding: 10'>
                    <span style='color: {chart_colors['O']}'>⬤</span> {cont[lang]['public']}
                    <span style='color: {chart_colors['P']}'>&nbsp;&nbsp;⬤</span> {cont[lang]['private']}
                    <span style='color: {chart_colors['F']}'>&nbsp;&nbsp;⬤</span> {cont[lang]['non_profit']}
                </p>
                """, unsafe_allow_html=True)



    # Write the SQL query to fetch the data
    query = """
    SELECT ht.treatment_code, hd.provider_type_code, td.treatment_name, 
        SUM(ht.treatment_count) sum_treatment_count, 
        SUM(hd.total_treatments) AS sum_total_treatments, 
        AVG(ht.treatment_count/total_treatments*100) AS avg_treatment_count_share
        FROM hospital_treatments AS ht
        INNER JOIN hospital_details AS hd ON hd.hospital_id = ht.hospital_id
        INNER JOIN treatments_dict AS td ON td.treatment_code = ht.treatment_code
        WHERE td.language_code = 'en' AND ht.treatment_count > 0
        GROUP BY ht.treatment_code, hd.provider_type_code, td.treatment_name;
    """
    engine = establish_connection_to_database()
    df_barchart = pd.read_sql(query, engine)

    # Sort by sum_total_treatments
    df_barchart = df_barchart.sort_values(by='sum_total_treatments', ascending=False)

    # Create the horizontal bar chart
    fig_barchart = px.bar(
        df_barchart,
        x='avg_treatment_count_share', 
        y='treatment_name', 
        color='provider_type_code',
        color_discrete_map=chart_colors,
        orientation='h',
        labels={
            'avg_treatment_count_share': 'Average Treatment Count Share (%)',
            'treatment_name': 'Treatment Name'
        },
        height=800,  # Adjust the height as needed
    )

    # Update layout to better organize the plot
    fig_barchart.update_layout(
        title={'text': 'Average Treatment Count Share by Treatment and Provider Type', 'x': 0.5, 'xanchor': 'center'},
        xaxis_title='Average Treatment Count Share (%)',
        yaxis_title='',
        barmode='group',  # Group bars together by treatment_name
        showlegend=False,
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig_barchart, use_container_width=True)



    # New bubble chart

    # Assuming you have already established a database connection and fetched the data into df_bubble_chart
    query = """
    SELECT ht.treatment_code, hd.provider_type_code, td.treatment_name, COUNT(ht.hospital_id) AS hospital_count, SUM(ht.treatment_count) sum_treatment_count, 
        SUM(hd.total_treatments) AS sum_total_treatments, 
        AVG(ht.treatment_count/total_treatments*100) AS avg_treatment_count_share
        FROM hospital_treatments AS ht
        INNER JOIN hospital_details AS hd ON hd.hospital_id = ht.hospital_id
        INNER JOIN treatments_dict AS td ON td.treatment_code = ht.treatment_code
        WHERE td.language_code = 'en' AND ht.treatment_count > 0
        GROUP BY ht.treatment_code, hd.provider_type_code, td.treatment_name;
    """
    engine = establish_connection_to_database()
    df_bubble_chart = pd.read_sql(query, engine)

    # Sort by sum_total_treatments
    df_bubble_chart = df_bubble_chart.sort_values(by='sum_total_treatments', ascending=False)

    # Create the bubble chart
    fig_bubble_chart = px.scatter(
        df_bubble_chart, 
        x='avg_treatment_count_share', 
        y='treatment_name', 
        size='hospital_count',  # Size of bubbles
        color='provider_type_code',
        color_discrete_map=chart_colors,
        hover_name='treatment_name',
        hover_data={'sum_treatment_count': True, 'avg_treatment_count_share': True, 'sum_total_treatments': True},
        size_max=20,  # Max bubble size
        height=800,  # Adjust height as needed
        labels={
            'sum_treatment_count': 'Sum of Treatment Count',
            'treatment_name': 'Treatment Name',
            'avg_treatment_count_share': 'Average Treatment Count Share (%)'
        }
    )

    # Update the layout
    fig_bubble_chart.update_layout(
        title={'text': 'Bubble Chart of Treatment Distribution by Provider Type', 'x': 0.5, 'xanchor': 'center'},
        xaxis_title='Sum of Treatment Count',
        yaxis_title='',
        yaxis=dict(categoryorder='total ascending'),  # Order treatments by total sum_treatment_count
        showlegend=False,
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig_bubble_chart, use_container_width=True)

    # Violin plot
    query = f"""
        WITH total_count_per_treatment AS
            (SELECT ht.treatment_code, SUM(ht.treatment_count) AS sum_treatment_count, AVG(ht.treatment_count) AS avg_treatment_count
                FROM hospital_treatments AS ht
                GROUP BY ht.treatment_code)
        SELECT ht.treatment_code, td.treatment_name, hd.provider_type_code, ht.treatment_count, tcpt.sum_treatment_count, tcpt.avg_treatment_count, (ht.treatment_count-tcpt.avg_treatment_count)/tcpt.avg_treatment_count AS relative_treatment_count
            FROM hospital_treatments AS ht
            INNER JOIN hospital_details AS hd ON hd.hospital_id = ht.hospital_id
            INNER JOIN treatments_dict AS td ON td.treatment_code = ht.treatment_code
            INNER JOIN total_count_per_treatment AS tcpt ON tcpt.treatment_code = ht.treatment_code
            WHERE td.language_code = 'en' AND ht.treatment_count > 0;
        """
    engine = establish_connection_to_database()
    df_treatments = pd.read_sql(query, engine)

    # Create a horizontal violin plot
    fig_treatments = go.Figure()

    # Loop through each provider type and add a violin trace for each treatment
    for provider_type in df_treatments['provider_type_code'].unique():
        for treatment_name in df_treatments['treatment_name'].unique():
            filtered_data = df_treatments[
                (df_treatments['provider_type_code'] == provider_type) & 
                (df_treatments['treatment_name'] == treatment_name)
            ]
            fig_treatments.add_trace(go.Violin(
                x=filtered_data['relative_treatment_count'],
                y=[treatment_name] * len(filtered_data),  # Repeat the treatment_name for y-axis
                line_color=chart_colors[provider_type],
                name=f"{treatment_name} ({provider_type})",
                fillcolor=chart_colors[provider_type],
                hoverinfo='x',
                opacity=0.6,  # Adjust the opacity as needed
                orientation='h',
            ))

    # Update layout for the figure
    fig_treatments.update_layout(
        xaxis_title='Relative Treatment Count',
        yaxis_title='Treatment Name',
        title={'text': 'Distribution of Relative Treatment Counts by Treatment and Provider Type', 'x': 0.5, 'xanchor': 'center'},
        showlegend=False,  # You can set this to True if you want a legend
        height=3000,  # Adjust height as needed to fit all treatments
        xaxis=dict(
            title='Relative Treatment Count',
            range=[-5, 50]  # Ensure x-axis has a bit of extra space
        ),
        yaxis=dict(
            title='Treatment Name',
            categoryorder='total ascending',  # Order treatments based on total
        )
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig_treatments, use_container_width=True)

    # Bar chart
    query = f"""
        SELECT ht.treatment_code, td.treatment_name, hd.provider_type_code, AVG(ht.treatment_count) AS avg_treatment_count, COUNT(ht.hospital_id) AS hospital_count, AVG(hd.bed_count) AS avg_bed_count
        FROM hospital_treatments AS ht
        INNER JOIN hospital_details AS hd ON hd.hospital_id = ht.hospital_id
        INNER JOIN treatments_dict AS td ON td.treatment_code = ht.treatment_code
        WHERE td.language_code = 'en' AND ht.treatment_count > 0
        GROUP BY ht.treatment_code, hd.provider_type_code, td.treatment_name;
        """
    engine = establish_connection_to_database()
    df_treatments = pd.read_sql(query, engine)
    df_treatments = df_treatments.sort_values(by=['avg_treatment_count'], ascending=True) 

    colors_treatments = [chart_colors[provider_type] for provider_type in df_treatments['provider_type_code']]

    fig_treatments = px.bar(
        df_treatments, x='hospital_count', y='treatment_name', color='provider_type_code', color_discrete_map=chart_colors,
        orientation='h'
    )
    fig_treatments.update_layout(
        xaxis=dict(title=''),
        yaxis=dict(title=''),
        title={'text': 'Number of hospitals providing specific treatments', 'x': 0.5, 'xanchor': 'center',},
        showlegend=False,
        height=800,
    )
    st.plotly_chart(fig_treatments, use_container_width=True)

    # Bubble chart

    # SQL query and data fetching
    query = """
        SELECT ht.treatment_code, td.treatment_name, hd.provider_type_code, AVG(ht.treatment_count) AS avg_treatment_count, SUM(ht.treatment_count) AS sum_treatment_count, COUNT(ht.hospital_id) AS hospital_count, AVG(hd.bed_count) AS avg_bed_count
        FROM hospital_treatments AS ht
        INNER JOIN hospital_details AS hd ON hd.hospital_id = ht.hospital_id
        INNER JOIN treatments_dict AS td ON td.treatment_code = ht.treatment_code
        WHERE td.language_code = 'en' AND ht.treatment_count > 0
        GROUP BY ht.treatment_code, hd.provider_type_code, td.treatment_name;
    """
    engine = establish_connection_to_database()
    df_treatments = pd.read_sql(query, engine)

    # Sort data by average treatment count if needed
    # Aggregate data to calculate the total hospital count per treatment across all provider types
    df_aggregated = df_treatments.groupby('treatment_code').agg(
        total_hospital_count=('hospital_count', 'sum'),
        total_treatment_count=('sum_treatment_count', 'sum')
    ).reset_index()

    # Merge the aggregated data back with the original data to maintain details for plotting
    df_treatments_merged = pd.merge(df_treatments, df_aggregated, on='treatment_code', suffixes=('', '_total'))

    # Sort data by the aggregated total hospital count
    df_treatments_sorted = df_treatments_merged.sort_values(by='total_treatment_count', ascending=True)

    colors_treatments = [chart_colors[provider_type] for provider_type in df_treatments_sorted['provider_type_code']]

    fig_treatments = px.scatter(
        df_treatments_sorted, 
        x='hospital_count', 
        y='treatment_name', 
        size='sum_treatment_count',  # Size of bubbles
        color='provider_type_code', 
        color_discrete_map=chart_colors,
        title='Number of Hospitals Providing Specific Treatments',
        labels={'hospital_count': 'Number of Hospitals', 'avg_treatment_count': 'Average Treatment Count'}
    )

    # Update layout for better visualization
    fig_treatments.update_layout(
        xaxis_title='',
        yaxis_title='',
        title={'text': 'Number of Hospitals Providing Specific Treatments', 'x': 0.5, 'xanchor': 'center'},
        showlegend=False,  # Show legend to differentiate provider types
        height=800
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig_treatments, use_container_width=True)


    # Nursing quotient vs. total stations
    query = """
        SELECT hd.hospital_id, hd.nursing_quotient, hd.total_stations_count, hd.provider_type_code
	    FROM hospital_details AS hd;
        """
    engine = establish_connection_to_database()
    df_nursing = pd.read_sql(query, engine)

    colors_nursing = [chart_colors[provider_type] for provider_type in df_nursing['provider_type_code']]
    
    fig_nursing = go.Figure(data=go.Scatter(
        x=df_nursing['total_stations_count'], y=df_nursing['nursing_quotient'],
        mode='markers', marker=dict(color=colors_nursing),
        )
    )
    fig_nursing.update_layout(
        xaxis_title='Total Stations',
        yaxis_title='Nursing Quotient',
        title={'text': 'Nursing Quotient vs. Total Stations in Hospitals', 'x': 0.55, 'xanchor': 'center', 'y': 0.85},
        showlegend=False
    )
    st.plotly_chart(fig_nursing, use_container_width=True)

    # Nursing staff vs. total stations
    query = """
        SELECT hd.hospital_id, hd.nursing_count, hd.total_stations_count, hd.provider_type_code
	    FROM hospital_details AS hd;
        """
    engine = establish_connection_to_database()
    df_nursing = pd.read_sql(query, engine)

    colors_nursing = [chart_colors[provider_type] for provider_type in df_nursing['provider_type_code']]
    
    fig_nursing = go.Figure(data=go.Scatter(
        x=df_nursing['total_stations_count'], y=df_nursing['nursing_count'],
        mode='markers', marker=dict(color=colors_nursing),
        )
    )
    fig_nursing.update_layout(
        xaxis_title='Total Stations',
        yaxis_title='Nursing Staff Count',
        title={'text': 'Nursing Staff Count vs. Total Stations in Hospitals', 'x': 0.55, 'xanchor': 'center', 'y': 0.85},
        showlegend=False
    )
    st.plotly_chart(fig_nursing, use_container_width=True)



# PLACES MAP PAGE
elif selected == cont[lang]['menu_places_map']:

    # Get places data
    query = """
        SELECT name, latitude, longitude, zip
        FROM places
        """
    engine = establish_connection_to_database()
    df_places = pd.read_sql(query, engine)
    df_places['zip'] = df_places['zip'].astype(int)

    # Create figures        
    if "mapstyle" not in ms:
        mapstyle = 'open-street-map'
    else:
        mapstyle = ms.mapstyle

    fig_places = create_places_map(df_places, mapstyle, chart_colors)

    with st.container():
        col1, col2, col3 = st.columns([1, 10, 1])

        with col2:
            # Render figures
            st.markdown(map_css(), unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; padding: 10'>{cont[lang]['places_map_title']}</h2>", unsafe_allow_html=True)
            st.plotly_chart(fig_places, use_container_width=True)