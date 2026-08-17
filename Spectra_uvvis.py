import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter
import os


def get_wavelengths():
    temp_data=[]
    PeakW_results=[]
    axis_results=[]
    x_values = []
    y_values = []
    points = []
    i = 1


    for line in my_file:
        # Strip whitespace and newline characters before splitting
        line = line.strip()
        if line:  # Check if the line is not empty
            temp_data += [line.split(',')]

    while i < len(temp_data):
        # Process the line containing sample name and coordinates, e.g., 'MollyTest1-y2-x8'
        sample_coord_line = temp_data[i][0]

        # Find the positions of '-y' and '-x' to extract the coordinates
        idx_y_prefix = sample_coord_line.find('-y')
        idx_x_prefix = sample_coord_line.find('-x')

        if idx_y_prefix != -1 and idx_x_prefix != -1:
            # Extract the y and x values as strings
            y_val_str = sample_coord_line[idx_y_prefix + 2 : idx_x_prefix] # '2' from 'MollyTest1-y2-x8'
            x_val_str = sample_coord_line[idx_x_prefix + 2 :] # '8' from 'MollyTest1-y2-x8'
            # Append them to axis_results in the format expected by the subsequent loop
            axis_results.append([f'y{y_val_str}', f'x{x_val_str}'])
        else:
            print(f"Warning: Could not parse y-x coordinates from line: '{sample_coord_line}'")

        # Extract numerical values using more robust string manipulation
        try:
            PeakW_results.append(float((temp_data[i + 5][0].split('=')[1]).strip('\n  nm')))
        except (IndexError, ValueError) as e:
            print(f"Error parsing data on line {i}: {e}")
        i = i + 9

    for n in range(0,len(axis_results)): #iterate over all of the values in the axis_results list
        y_value_str = axis_results[n][0].strip('y')
        x_value_str = axis_results[n][1].strip('x')
        if y_value_str and x_value_str: # Check if strings are not empty
            y_values.append(float(y_value_str)) #adds all of the y values to a list called y_values
            x_values.append(float(x_value_str)) #adds all of the x values to a list called x_values
            points.append([float(x_value_str),float(y_value_str)])
    for i in range(0,len(temp_data[1][0])): #iterates over the first sample name in the results text file
        if temp_data[1][0][i:i+2] == '-y': #if two characters next to each other are '-y'
            Name_of_File = temp_data[1][0][0:i] #Name_of_File is the string before those two characters


    points = np.array(points) #Makes an array of the x and y points
    grid_x, grid_y = np.mgrid[2.5:max(x_values):950j, 2.5:max(y_values):500j] #Creates our x and y grid from 2.5 to max x/y value with 1,000 and 2,000 points, changed 750,250 to 950 & 500
    from scipy.interpolate import griddata
    grid_z0orig = griddata(points, PeakW_results, (grid_x, grid_y), method='nearest') #
    grid_z0 = gaussian_filter(grid_z0orig,6)
    return PeakW_results
    # plt.figure(figsize=(10,3))                 #new figure
    # plt.title('Wavelength (nm)')
    # plt.xlim(0,80)                              #sets the x axis limit to highest x value with 2.5 border, changed 75 to 95
    # plt.ylim(0,30)                              #sets the y axis limit to highest y value with 2.5 border, changed 25 to 50
    # plt.imshow(grid_z0.T, extent=(0,max(x_values),0,max(y_values)), origin='lower',cmap='coolwarm',vmin=minv,vmax=maxv)
    # cbar=plt.colorbar(label='Wavelength (nm)') #Creates a colorbar for the transmission / wavelength
    # #plt.title("{} {} ({})".format(Names[l].split()[0],Names[l].split()[1],Name_of_File)) #Allows us to iterate through the different data titles
    # save_path = os.path.join(output_loc, f'peakW_{Name_of_File}.svg')
    # plt.savefig(save_path, bbox_inches='tight') #Save different data titles as pdf
    # plt.show()

def transmission_vs_wl():

    possible_peakW_keys = [key for key in opf.keys() if 'int' in key.lower()]
    if not possible_int_keys:
        raise KeyError(f"No intensity map found in {asdf_file}")
    int_key = possible_int_keys[0]
    int_map = af.tree[int_key]

    possible_dopp_keys = [key for key in af.tree.keys() if 'dopp' in key.lower()]
    if not possible_dopp_keys:
        raise KeyError(f"No Doppler map found in {asdf_file}")
    dopp_key = possible_dopp_keys[0]
    dopp_map = af.tree[dopp_key]

    possible_width_keys = [key for key in af.tree.keys() if 'width' in key.lower()]
    if not possible_width_keys:
        raise KeyError(f"No width map found in {asdf_file}")
    width_key = possible_width_keys[0]
    width_map = af.tree[width_key]

    possible_vnt_keys = [key for key in af.tree.keys() if 'vnt' in key.lower()]
    if possible_vnt_keys:
        vnt_key = possible_vnt_keys[0]
        vnt_map = af.tree[vnt_key]
    else:
        vnt_map = None
        print(f'Warning: No VNT map found in {asdf_file}. Skipping vnt plot.')

    possible_asym_keys = [key for key in af.tree.keys() if 'asym' in key.lower()]
    if not possible_asym_keys:
        raise KeyError(f"No asym map found in {asdf_file}")
    asym_key = possible_asym_keys[0]
    asym_map = af.tree[asym_key]

    #PLOTTING
    plt.figure()
    plt.plot(PeakT_results,'r-')
    plt.plot(PeakW_results,'b-')

output_loc = r"C:\Users\molly\OneDrive\Masters\Data\MT1\Outputs"
input_loc = r"C:\Users\molly\OneDrive\Masters\Data\MT1"
my_file = open(os.path.join(input_loc,"MT1.zip"))
minv = 350
maxv = 750

transmission_vs_wl()
