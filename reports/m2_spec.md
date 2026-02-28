# Updated Job Stories

# Component Iventory
| ID                               | Type          | Shiny widget / renderer                        | Depends on                                  | Job story                |
|----------------------------------|---------------|------------------------------------------------|---------------------------------------------|--------------------------|
| Date/Year                        | Input         | ui.input_slider()                              | —                                           |                          |
| State                            | Input         | ui.input_select()                              | —                                           |                          |
| City                             | Input         | ui.input_selectize()                              | —                                           |                          |
| Population                       | Input         | ui.input_slider()                              | —                                           |                          |
| Category                         | Input         | ui.input_select()                              | —                                           |                          |
| Aggregate Crime Column           | Input         | ui.input_slider()                              | —                                           |                          |
| filtered_df                      | Reactive calc | @reactive.calc                                 | input_year, input_region                    | #1, #2, #3               |
| filtered_data                    | Reactive calc | @reactive.calc                                 | input_year                                  |                          |
| most_common_crime                | Reactive calc | @reactive.calc                                 | filtered_data                               |                          |
| crime_range_table                | Reactive calc | @reactive.calc                                 | filtered_data                               |                          |
| KPI (Total Crime)                | Output        | @reactive.text; ui.value_box("name"           | ui.output_text(""name_from_server_func"")) | input_year, input_region |
| KPI (Crime Rate)                 | Output        | @reactive.text; ui.value_box("name"           | ui.output_text(""name_from_server_func"")) | filtered_df              |
| KPI (population)                 | Output        | @reactive.text; ui.value_box("name"           | ui.output_text(""name_from_server_func"")) | filtered_df              |
| KPI (Most Common Crime)          | Output        | @reactive.text; ui.value_box("name"           | ui.output_text(""name_from_server_func"")) |                          |
| KPI (Change in Crime Rate) Table | Output        | @render.data_frame                             |                                             |                          |
| Map Graph                        | Output        | @render.widget; ui.ouput_widget("plot_name")   |                                             |                          |
| Line graph (Comparision)         | Output        | @render.widget; ui.ouput_widget("plot_name")   | filtered_df                                 |                          |

# Reactivity Diagram

# Calculation Details
For the `filtered_df` reactive calculation, we will filter the original dataset based on the user’s selections for year, state, city, total crime range, crime category and population filters. This will allow us to create a subset of the data that is relevant to the user’s specific interests and needs. This filtered dataset is used to output the Crime over time line graph and all KPI summaries.

For the `filtered_data` reactive calculation, we will filter the original dataset based on the user’s selection for the year. This dataset is used to subset the data for the `most_common_crime` and `crime_change_table` reactive calculations.

For the `most_common_crime` reactive calculation, we will analyze the `filtered_data` dataset to determine which crime category has the highest count for the selected year range. This will allow us to output the most common crime as a KPI.

For the `crime_range_table` reactive calculation, we will analyze the `filtered_data` dataset to calculate the change in crime rates over time for each crime category. This will allow us to output a table that shows how crime rates have changed for each category, which can help users understand trends and patterns in crime over time.