# Indoor_Localization

This is a project done as a part of the course Smart Sensing for IoT
which deals with Trilateration of a Node in a 100x100 grid given the range measurements from
3 access points (APs).

Both Brute force methods as well as Least Squares Optimization methods using LMFIT are used
to trilaterate and analyse error performance and time.

<img src='https://user-images.githubusercontent.com/64144419/126334974-f5ac67a3-d6f2-4341-aa1b-deeb2db9f098.png' height=300> <img src='https://user-images.githubusercontent.com/64144419/126334171-01c30e68-4887-4ce1-b9a2-cc078cfdeeba.png' height=300>
<img src='https://user-images.githubusercontent.com/64144419/126333738-2e900c67-37df-4311-a7bd-1c3440e2a2e4.png' width=500>
<img src='https://user-images.githubusercontent.com/64144419/126333864-43fa5c89-65c2-47a9-b708-d7bacc9b1c1c.png' width=300>

The detailed report on Dataset Generation, Localization, Observations, Impact of Anchor Points
and Geometric Dilution of Precision can be found [here]().

## Dependencies
* LMFIT
* Numpy
* Matplotlib
* AST
* argparse
* linecache, math, os
* bash commands - ls, grep, xargs, rm

## generate_dataset.py
Generates the following dataset:

![image](https://user-images.githubusercontent.com/64144419/126333051-f28600da-2970-4909-af0d-1adf3d2b7fd8.png)

>Running this file deletes old dataset files if present. Hence backup if necessary. It also
asks for conformation while running.

To run: `python3 generate_dataset.py`

## brute_force_localization.py
This displays a random heatmap of rms cost function each time you run it.

To run: `python3 brute_force_localization.py`

![image](https://user-images.githubusercontent.com/64144419/126333386-2520a302-2647-418e-b633-53cb544c6622.png)

## trilaterization.py
Generates the following trilaterization data depending on the brute-step given:

![image](https://user-images.githubusercontent.com/64144419/126333172-319eda73-efc3-457f-aed2-0b2ddcbedb46.png)

>Running this file deletes corresponding old trilaterization files if present. Hence backup if
necessary. It also asks for conformation while running.

To run: `python3 trilaterization.py [--brute_step {int}]`

If no brute_step if given it defaults to using (50,50) as starting point.
Brute Step 10 and 5 take atleast 30mins to complete.

## trilaterization_errors_per_range_error.py
Generates 3 plots and prints some useful information in the terminal as given in the report.
Use q to navigate from one plot to the next.
Shows CDF, PDF and Violin Plot.
![image](https://user-images.githubusercontent.com/64144419/126333675-45bfa28e-2874-466c-9a52-2da739c10893.png)
![image](https://user-images.githubusercontent.com/64144419/126334061-f8e1fb7c-8f3c-42bc-8b17-005555624f9c.png)

To run: `python3 trilaterization_errors_per_range_error.py [--file_id {brute_step}]`

`file_id` is the prefix of the files to be used which happens to be the `brute_step`. If nothing is given it defaults to
using files which have prefix "_" which corresponds to starting point (50,50).

## trilateration_errors_per_anchor_triplet.py
Generates a bar graph plot of median errors per anchor configuration.
![image](https://user-images.githubusercontent.com/64144419/126334263-8121a93e-6f35-4e01-b832-88def0b66f40.png)

To run: `python3 trilaterization_errors_per_anchor_triplet.py [--file_id {brute_step}] [--show_before_after]`

`file_id` is same as the previous script.
The `show_before_after` flag displays the scatter plot for each anchor triplet. Since, 400 plots have to be seen to
end the script, Ctrl+C can be used to end the script.
Each time the script is run a random range error order is used so that you don't have to see all 100 before going to
the next one.
Both the flags can be used in combination to read different brute_step files.
Use q to navigate from one plot to the next.
![image](https://user-images.githubusercontent.com/64144419/126334294-a9271b65-9aab-423b-9a9e-0df7c9e62bb8.png)
