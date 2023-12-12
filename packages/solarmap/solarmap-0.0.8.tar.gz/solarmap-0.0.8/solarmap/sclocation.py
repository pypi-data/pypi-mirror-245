# author L Alberto Canizares canizares@cp.dias.ie
import matplotlib.pyplot as plt
from datetime import datetime as dt
from datetime import timedelta
#import astropy.units as u
from astropy.constants import c, m_e, R_sun, e, eps0, au
import numpy as np
import sys

#from sunpy.time import parse_time
from sunpy.coordinates import get_horizons_coord


def cart2pol(x, y):
    # Calculate radius (r)
    r = np.sqrt(x ** 2 + y ** 2)

    # Calculate angle (theta) in radians
    theta = np.arctan2(y, x)

    # Convert angle to degrees if needed
    theta_degrees = np.degrees(theta)

    return r, theta_degrees

def help():
    # UPDATE HELP
    string = f" ---------- SolarMAP ---------- " \
             f"SolarMap generates a map of the solarsystem and returns HEE coordinates\n" \
             f"SolarMap simplifies the usage of  sunpy.coordinates import get_horizons_coord\n" \
             f"get_HEE_coord returns an array with positions of objects in solar sytem in HEE\n" \
             f"\n"\
             f"" \
             f"\n" \
             f"date: year:int\n" \
             f"      \tmonth:int\n" \
             f"      \tday:int\n" \
             f"objects: list of strings with object ids\n" \
             f"timeres:int  -  time resolution in hours for positions.\n" \
             f"         \t24: 1 position every 24 hours\n" \
             f"         \t1: 1 position for every hour of the day" \
             f"\n"
    string2 = f"USAGE:\n" \
              f"----------------------------" \
              f"\n" \
              f"# Show suported spacecraft: run: get_HEE_coord.show_spacecraft_ids(get_HEE_coord) \n" \
              f"find supported objects:" \
              f"from sunpy.coordinates import get_horizons_coord " \
              f"objects = ['sun', 'mars express', 'earth', 'venus', 'psp', 'solo', 'tesla']\n" \
              f"\n" \
              f"# Generate map\n" \
              f"solarsystem = solarmap.get_sc_coord(date=[2021, 6, 26], objects=objects,orbitlength=100, timeres=24)\n" \
              f"\n" \
              f"# gives the location of the objects at the specified DATE without orbits or labels.\n" \
              f"simple_coord_rsun = np.array(solarsystem.locate_simple())\n" \
              f"\n" \
              f"# Plotting map of objects\n" \
              f"figure = solarsystem.plot()\n" \
              f"\n" \
              f"# Verbose version of coordinates with orbit, with labels. the last position is the specified date.\n" \
              f"coord_rsun = solarsystem.locate()\n"
    print(string)
    print(string2)

class get_sc_coord:
    print("WARNING: get_sc_coord soon to be deprecated. Please use get_HEE_coord")
    def __init__(self, date=[], objects=[""], orbit=0, orbitlength=1, timeres=24):
        self.date = date
        self.objects = objects
        self.orbit = orbit
        self.orbitlength = orbitlength
        self.timeres = timeres        # in hours

        if orbitlength < 1:
            print(f"WARNING: orbitlength must be set to 1 or higher. Corrected")
            self.orbitlength = 1

    def buff_locate(self):
        date = self.date
        objects = self.objects
        orbit = self.orbit
        orbitlength = self.orbitlength
        timeres = self.timeres

        print(f"Objects: {objects}")
        locations = []
        locations_v = {}

        # Constants
        r_sun = R_sun.value  # km
        AU = au.value  # km

        day = date[2]
        month = date[1]
        year = date[0]

        targetday = dt(year, month, day)

        starttime = targetday - timedelta(days=orbitlength)
        endtime = targetday
        # times = []
        # while starttime < endtime:
        #     times.append(starttime)
        #     starttime += timedelta(hours=timeres)
        for object in objects:
            if "sun" == object:
                sun_x = 0
                sun_y = 0
                sunz_z = 0
                locations.append([sun_x,sun_y])
                locations_v["sun"] = [sun_x,sun_y, sunz_z]

            if "mercury" == object:
                #Mercury location
                mercury_coord = get_horizons_coord("Mercury Barycenter", time={'start': starttime,
                                                                               'stop': endtime,
                                                                               'step':f"{orbitlength}"}, id_type=None)
                mercury_xyz = mercury_coord.heliocentricearthecliptic.cartesian.get_xyz()[:].value * (AU / r_sun)
                locations.append([mercury_xyz[0][-1], mercury_xyz[1][-1]])
                locations_v["mercury"] = mercury_xyz[:,1:]
            if "venus" == object:
                # VENUS POSITION
                venus_coord = get_horizons_coord("Venus Barycenter", time={'start': starttime,
                                                                               'stop': endtime,
                                                                               'step':f"{orbitlength}"}, id_type=None)
                venus_xyz = venus_coord.heliocentricearthecliptic.cartesian.get_xyz()[:].value * (AU / r_sun)
                locations.append([venus_xyz[0][-1],venus_xyz[1][-1]])
                locations_v["venus"] = venus_xyz[:,1:]


            if "earth" == object:
                # Earth location
                earth_coord = get_horizons_coord("Earth-Moon Barycenter", time={'start': starttime,
                                                                               'stop': endtime,
                                                                               'step':f"{orbitlength}"}, id_type=None)
                earth_xyz = earth_coord.heliocentricearthecliptic.cartesian.get_xyz()[:].value*(AU/r_sun)
                locations.append([earth_xyz[0][-1],earth_xyz[1][-1]])
                locations_v["earth"] = earth_xyz[:,1:]

            if "mars" == object:
                # Earth location
                mars_coord = get_horizons_coord("Mars Barycenter", time={'start': starttime,
                                                                               'stop': endtime,
                                                                               'step':f"{orbitlength}"}, id_type=None)
                mars_xyz = mars_coord.heliocentricearthecliptic.cartesian.get_xyz()[:].value*(AU/r_sun)
                locations.append([mars_xyz[0][-1],mars_xyz[1][-1]])
                locations_v["mars"] = mars_xyz[:,1:]

            if "psp" == object:
                # PSP location
                psp_coord = get_horizons_coord("PSP", time={'start': starttime,
                                                            'stop': endtime,
                                                            'step':f"{orbitlength}"}, id_type=None)
                psp_xyz = psp_coord.heliocentricearthecliptic.cartesian.get_xyz()[:].value * (AU / r_sun)
                locations.append([psp_xyz[0][-1],psp_xyz[1][-1]])
                locations_v["psp"] = psp_xyz[:,1:]


            if "solo" == object:
                # 2020-FEB-10 04:56:58.8550
                solo_coord = get_horizons_coord("SOLO", time={'start': starttime,
                                                              'stop': endtime,
                                                              'step':f"{orbitlength}"}, id_type=None)
                solo_xyz = solo_coord.heliocentricearthecliptic.cartesian.get_xyz()[:].value * (AU / r_sun)
                locations.append([solo_xyz[0][-1],solo_xyz[1][-1]])
                locations_v["solo"] = solo_xyz[:,1:]

            if "stereo_a"== object:
                # STEREO A POSITION
                stereoa_coord = get_horizons_coord("STEREO-A", time={'start': starttime,
                                                                     'stop': endtime,
                                                                     'step':f"{orbitlength}"}, id_type=None)
                stereoa_xyz = stereoa_coord.heliocentricearthecliptic.cartesian.get_xyz()[:].value * (AU / r_sun)
                locations.append([stereoa_xyz[0][-1],stereoa_xyz[1][-1]])
                locations_v["stereo_a"] = stereoa_xyz[:,1:]

                ##

            if "stereo_b" == object:
                # STEREO B POSITION
                stereob_coord = get_horizons_coord("STEREO-B", time={'start': starttime,
                                                                     'stop': endtime,
                                                                     'step':f"{orbitlength}"}, id_type=None)
                stereob_xyz = stereob_coord.heliocentricearthecliptic.cartesian.get_xyz()[:].value * (AU / r_sun)
                locations.append([stereob_xyz[0][-1],stereob_xyz[1][-1]])
                locations_v["stereo_b"] = stereob_xyz[:,1:]

                ##

            if "wind" == object:
                ephemeris_available = dt(2019,10,8,0,1,10)
                if starttime >= ephemeris_available:
                    # wind location is in Sun - Earth L1
                    wind_coord = get_horizons_coord("Wind (spacecraft)", time={'start': starttime,
                                                                  'stop': endtime,
                                                                  'step':f"{orbitlength}"}, id_type=None)
                    wind_xyz = wind_coord.heliocentricearthecliptic.cartesian.get_xyz()[:].value * (AU / r_sun)
                    locations.append([wind_xyz[0][-1],wind_xyz[1][-1]])
                    locations_v["wind"] = wind_xyz[:,1:]
                else:
                    # SOHO and WIND are both located near L1
                    print("WARNING: No ephemeris for target Wind (spacecraft) prior to A.D. 2019-OCT-08 00:01:09.1823 TD")
                    print("Assuming L1.")
                    wind_coord = get_horizons_coord("SEMB-L1", time={'start': starttime,
                                                                  'stop': endtime,
                                                                  'step':f"{orbitlength}"}, id_type=None)
                    wind_xyz = wind_coord.heliocentricearthecliptic.cartesian.get_xyz()[:].value * (AU / r_sun)
                    locations.append([wind_xyz[0][-1],wind_xyz[1][-1]])
                    locations_v["wind"] = wind_xyz[:,1:]

            if "soho" == object:
                soho_coord = get_horizons_coord("soho", time={'start': starttime,
                                                              'stop': endtime,
                                                              'step': f"{orbitlength}"}, id_type=None)
                soho_xyz = soho_coord.heliocentricearthecliptic.cartesian.get_xyz()[:].value * (AU / r_sun)
                locations.append([soho_xyz[0][-1], soho_xyz[1][-1]])
                locations_v["soho"] = soho_xyz[:, 1:]

            if "ace" == object:
                ace_coord = get_horizons_coord("ACE (spacecraft)", time={'start': starttime,
                                                              'stop': endtime,
                                                              'step': f"{orbitlength}"}, id_type=None)
                ace_xyz = ace_coord.heliocentricearthecliptic.cartesian.get_xyz()[:].value * (AU / r_sun)
                locations.append([ace_xyz[0][-1], ace_xyz[1][-1]])
                locations_v["ace"] = ace_xyz[:, 1:]

            if "bepicolombo" == object:
                # wind location is in Sun - Earth L1
                bepi_coord = get_horizons_coord("BepiColombo", time={'start': starttime,
                                                              'stop': endtime,
                                                              'step':f"{orbitlength}"}, id_type=None)
                bepi_xyz = bepi_coord.heliocentricearthecliptic.cartesian.get_xyz()[:].value * (AU / r_sun)
                locations.append([bepi_xyz[0][-1],bepi_xyz[1][-1]])
                locations_v["bepicolombo"] = bepi_xyz[:,1:]

        return locations, locations_v

    def locate_simple(self):
        out, _ = self.buff_locate()
        return out
    def locate(self):
        _, out = self.buff_locate()
        return out

    def plot(self):
        date = self.date
        objects = self.objects
        orbit = self.orbit
        orbitlength = self.orbitlength
        timeres = self.timeres


        day = date[2]
        month = date[1]
        year = date[0]


        if orbitlength > 1:
            plot_orbit = True
        else:
            plot_orbit = False
        locations_simple, locations_v = self.buff_locate()
        r_sun = R_sun.value  # km
        AU = au.value  # km

        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        lim_plot = AU / r_sun + 15
        ax.set(xlim=(-lim_plot, lim_plot), ylim=(-lim_plot, lim_plot))

        if "sun" in objects:
            # circle for the sun
            sun_xyz = locations_v["sun"]
            sun = plt.Circle((0, 0), 10, color='gold', fill=True)
            ax.add_artist(sun)

        if "mercury" in objects:
            mercury_xyz = locations_v["mercury"]
            mercury_location = plt.plot(mercury_xyz[0][-1], mercury_xyz[1][-1], 'go')
            plt.text(np.array(mercury_xyz[0][-1]) + 1, np.array(mercury_xyz[1][-1]) + 1, 'Mercury')
            r_m = np.sqrt(mercury_xyz[0][-1] ** 2 + mercury_xyz[1][-1] ** 2)
            circle_m = plt.Circle((0, 0), r_m, color='k', fill=False, linestyle='--', linewidth=1)
            ax.add_artist(circle_m)
            if plot_orbit == True:
                plt.plot(mercury_xyz[0], mercury_xyz[1], 'k-')

        if "venus" in objects:
            venus_xyz = locations_v["venus"]
            venus_location = plt.plot(venus_xyz[0][-1], venus_xyz[1][-1], 'go')
            plt.text(np.array(venus_xyz[0][-1]) + 1, np.array(venus_xyz[1][-1]) + 1, 'Venus')
            r_v = np.sqrt(venus_xyz[0][-1] ** 2 + venus_xyz[1][-1] ** 2)
            circle_v = plt.Circle((0, 0), r_v, color='k', fill=False, linestyle='--', linewidth=1)
            ax.add_artist(circle_v)
            if plot_orbit == True:
                plt.plot(venus_xyz[0], venus_xyz[1], 'k-')


        if "earth" in objects:
            earth_xyz = locations_v["earth"]
            earth_location = plt.plot(earth_xyz[0][-1], earth_xyz[1][-1], 'bo')
            plt.text(np.array(earth_xyz[0][-1]) + 1, np.array(earth_xyz[1][-1]) + 1, 'Earth')
            r_e = np.sqrt(earth_xyz[0][-1] ** 2 + earth_xyz[1][-1] ** 2)
            circle_e = plt.Circle((0, 0), r_e, color='k', fill=False, linestyle='--', linewidth=1)
            ax.add_artist(circle_e)
            if plot_orbit == True:
                plt.plot(earth_xyz[0], earth_xyz[1], 'k-')
        if "mars" in objects:
            mars_xyz = locations_v["mars"]
            mars_location = plt.plot(mars_xyz[0][-1], mars_xyz[1][-1], 'ro')
            plt.text(np.array(mars_xyz[0][-1]) + 1, np.array(mars_xyz[1][-1]) + 1, 'Mars')
            r_m = np.sqrt(mars_xyz[0][-1] ** 2 + mars_xyz[1][-1] ** 2)
            circle_m = plt.Circle((0, 0), r_m, color='k', fill=False, linestyle='--', linewidth=1)
            ax.add_artist(circle_m)
            if plot_orbit == True:
                plt.plot(mars_xyz[0], mars_xyz[1], 'k-')

        if "psp" in objects:
            psp_xyz = locations_v["psp"]
            psplocation = plt.plot(psp_xyz[0][-1], psp_xyz[1][-1], 'ro')
            plt.text(np.array(psp_xyz[0][-1]) + 1, np.array(psp_xyz[1][-1]) + 1, 'PSP')
            if plot_orbit == True:
                plt.plot(psp_xyz[0], psp_xyz[1], 'r-')

        if "solo" in objects:
            solo_xyz = locations_v["solo"]
            sololocation = plt.plot(solo_xyz[0][-1], solo_xyz[1][-1], 'ro')
            plt.text(np.array(solo_xyz[0][-1]) + 1, np.array(solo_xyz[1][-1]) + 1, 'Solar Orbiter')
            if plot_orbit == True:
                plt.plot(solo_xyz[0], solo_xyz[1], 'r-')

        if "stereo_a" in objects:
            stereoa_xyz = locations_v["stereo_a"]
            stereo_a_location = plt.plot(stereoa_xyz[0][-1], stereoa_xyz[1][-1], 'ko')
            plt.text(np.array(stereoa_xyz[0][-1]) + 1, np.array(stereoa_xyz[1][-1]) + 1, 'Stereo A')
            if plot_orbit == True:
                plt.plot(stereoa_xyz[0], stereoa_xyz[1], 'k-')
        if "stereo_b" in objects:
            stereob_xyz = locations_v["stereo_b"]
            stereo_b_location = plt.plot(stereob_xyz[0][-1], stereob_xyz[1][-1], 'ko')
            plt.text(np.array(stereob_xyz[0][-1]) + 1, np.array(stereob_xyz[1][-1]) + 1, 'Stereo B')
            if plot_orbit == True:
                plt.plot(stereob_xyz[0], stereob_xyz[1], 'k-')
        if "bepicolombo" in objects:
            bepi_xyz = locations_v["bepicolombo"]
            bepi_location = plt.plot(bepi_xyz[0][-1], bepi_xyz[1][-1], 'ko')
            plt.text(np.array(bepi_xyz[0][-1]) + 1, np.array(bepi_xyz[1][-1]) + 1, 'BepiColombo')
            if plot_orbit == True:
                plt.plot(bepi_xyz[0], bepi_xyz[1], 'k-')
        if "wind" in objects:
            wind_xyz = locations_v["wind"]
            windlocation = plt.plot(wind_xyz[0][-1], wind_xyz[1][-1], 'co')
            plt.text(wind_xyz[0][-1] - 20, wind_xyz[1][-1] + 1, 'wind')
            if plot_orbit == True:
                plt.plot(wind_xyz[0], wind_xyz[1], 'k-')


        lim_plot = np.max(np.absolute(locations_simple)) + 15   # automatically selects boundary of map based on outermost object
        # lim_plot = 1.5*AU / r_sun + 15
        ax.set(xlim=(-lim_plot, lim_plot), ylim=(-lim_plot, lim_plot))


        month_strings = {
            1: 'Jan',
            2: 'Feb',
            3: 'Mar',
            4: 'Apr',
            5: 'May',
            6: 'Jun',
            7: 'Jul',
            8: 'Aug',
            9: 'Sep',
            10: 'Oct',
            11: 'Nov',
            12: 'Dec'}

        ax.set_title(f'Spacecraft Coordinates - {day} / {month_strings[month]} / {year}', fontsize=18)
        ax.set_xlabel('HEE - X / $R_{\odot}$', fontsize=14)
        ax.set_ylabel('HEE - Y / $R_{\odot}$', fontsize=14)
        ax.grid()

        plt.show(block=False)
        return plt.gcf()



class get_HEE_coord:
    def __init__(self, date=[], objects=[""], orbit=0, orbitlength=1, timeres=24):
        self.date = date
        self.objects = objects
        self.orbit = orbit
        self.orbitlength = orbitlength
        self.timeres = timeres        # in hours
        if orbitlength < 1:
            print(f"WARNING: orbitlength must be set to 1 or higher. Corrected")
            self.orbitlength = 1

    def planet_ids(self, object=""):
        # simplifying planet names
        if object.capitalize() == "Mercury": object = "Mercury Barycenter"
        elif object.capitalize() == "Venus": object = "Venus Barycenter"
        elif object.capitalize() == "Earth" : object = "Earth-Moon Barycenter"  #
        elif object.capitalize() == "Mars": object = "Mars Barycenter"          #
        elif object.capitalize() == "Jupiter": object = "Jupiter Barycenter"    #
        elif object.capitalize() == "Saturn": object = "Saturn Barycenter"      #
        elif object.capitalize() == "Uranus": object = "Uranus Barycenter"      #
        elif object.capitalize() == "Neptune": object = "Neptune Barycenter"    #
        elif object.capitalize() == "Pluto": object = "Pluto Barycenter"        #
        elif object =="":
            print("mercury, venus, earth, mars, saturn, uranus, neptune, pluto")
        else:
            return object
        return object

    def simple_planet_ids(self, object=""):
        # simplifying planet names
        if object == "Mercury Barycenter": object = "mercury"
        elif object == "Venus Barycenter" : object = "venus"
        elif object == "Earth-Moon Barycenter" : object =  "earth"  #
        elif object == "Mars Barycenter": object = "mars"   #
        elif object == "Jupiter Barycenter"  : object ="jupiter" #
        elif object == "Saturn Barycenter"  : object = "saturn" #
        elif object == "Uranus Barycenter" : object = "uranus" #
        elif object == "Neptune Barycenter" : object ="neptune" #
        elif object == "Pluto Barycenter"   : object ="pluto"#
        else:
            return object
        return object

    def buff_locate(self):
        date = self.date
        objects = self.objects
        orbit = self.orbit
        orbitlength = self.orbitlength
        timeres = self.timeres

        print(f"Objects: {objects}")
        locations = []
        locations_v = {}

        # Constants
        r_sun = R_sun.value  # km
        AU = au.value  # km

        day = date[2]
        month = date[1]
        year = date[0]

        targetday = dt(year, month, day)

        starttime = targetday - timedelta(days=orbitlength)
        endtime = targetday
        # times = []
        # while starttime < endtime:
        #     times.append(starttime)
        #     starttime += timedelta(hours=timeres)

        for object in objects:
            object = self.planet_ids(object)
            if "wind" == object:
                ephemeris_available = dt(2019,10,8,0,1,10)
                if starttime >= ephemeris_available:
                    # wind location is in Sun - Earth L1
                    wind_coord = get_horizons_coord("Wind (spacecraft)", time={'start': starttime,
                                                                  'stop': endtime,
                                                                  'step':f"{orbitlength}"}, id_type=None)
                    wind_xyz = wind_coord.heliocentricearthecliptic.cartesian.get_xyz()[:].value * (AU / r_sun)
                    locations.append([wind_xyz[0][-1],wind_xyz[1][-1]])
                    locations_v["wind"] = wind_xyz[:,1:]
                else:
                    # SOHO and WIND are both located near L1
                    print("WARNING: No ephemeris for target Wind (spacecraft) prior to A.D. 2019-OCT-08 00:01:09.1823 TD")
                    print("Assuming L1.")
                    wind_coord = get_horizons_coord("SEMB-L1", time={'start': starttime,
                                                                  'stop': endtime,
                                                                  'step':f"{orbitlength}"}, id_type=None)
                    wind_xyz = wind_coord.heliocentricearthecliptic.cartesian.get_xyz()[:].value * (AU / r_sun)
                    locations.append([wind_xyz[0][-1],wind_xyz[1][-1]])
                    locations_v["wind"] = wind_xyz[:,1:]

            else:
                # wind location is in Sun - Earth L1
                object_coord = get_horizons_coord(object, time={'start': starttime,
                                                              'stop': endtime,
                                                              'step':f"{orbitlength}"}, id_type=None)
                object_xyz = object_coord.heliocentricearthecliptic.cartesian.get_xyz()[:].value * (AU / r_sun)
                locations.append([object_xyz[0][-1],object_xyz[1][-1]])
                locations_v[object] = object_xyz[:,1:]


        return locations, locations_v

    def locate_simple(self):
        out, _ = self.buff_locate()
        return out
    def locate(self):
        _, out = self.buff_locate()
        return out

    def plot(self):
        date = self.date
        objects = self.objects
        orbit = self.orbit
        orbitlength = self.orbitlength
        timeres = self.timeres


        day = date[2]
        month = date[1]
        year = date[0]


        if orbitlength > 1:
            plot_orbit = True
        else:
            plot_orbit = False
        locations_simple, locations_v = self.buff_locate()
        r_sun = R_sun.value  # km
        AU = au.value  # km

        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        lim_plot = AU / r_sun + 15
        ax.set(xlim=(-lim_plot, lim_plot), ylim=(-lim_plot, lim_plot))

        for obj in objects:
            obj = self.planet_ids(obj)
            lowercase_input = obj.lower()
            obj_xyz = locations_v[obj]
            center = (0, 0)
            radius, _ = cart2pol(obj_xyz[0][-1], obj_xyz[1][-1])
            # Check if the lowercase target word appears in the lowercase input string


            if "spacecraft" in lowercase_input:
                color_marker = 'k'
            elif "sun" in lowercase_input:
                color_marker = 'y'
            elif "mercury" in lowercase_input:
                color_marker = 'grey'
                circle = plt.Circle(center, radius, edgecolor='grey', facecolor='none', linestyle='dashed')
                ax.add_patch(circle)
            elif "venus" in lowercase_input:
                color_marker = 'y'
                circle = plt.Circle(center, radius, edgecolor='grey', facecolor='none', linestyle='dashed')
                ax.add_patch(circle)
            elif "earth" in lowercase_input:
                color_marker = 'b'
                circle = plt.Circle(center, radius, edgecolor='grey', facecolor='none', linestyle='dashed')
                ax.add_patch(circle)
            elif "mars" in lowercase_input:
                color_marker = 'r'
                circle = plt.Circle(center, radius, edgecolor='grey', facecolor='none', linestyle='dashed')
                ax.add_patch(circle)
            elif "jupiter" in lowercase_input:
                color_marker = 'r'
                circle = plt.Circle(center, radius, edgecolor='grey', facecolor='none', linestyle='dashed')
                ax.add_patch(circle)
            elif "saturn" in lowercase_input:
                color_marker = 'y'
                circle = plt.Circle(center, radius, edgecolor='grey', facecolor='none', linestyle='dashed')
                ax.add_patch(circle)
            elif "uranus" in lowercase_input:
                color_marker = 'c'
                circle = plt.Circle(center, radius, edgecolor='grey', facecolor='none', linestyle='dashed')
                ax.add_patch(circle)
            elif "neptune" in lowercase_input:
                color_marker = 'b'
                circle = plt.Circle(center, radius, edgecolor='grey', facecolor='none', linestyle='dashed')
                ax.add_patch(circle)
            else:
                color_marker = 'k'

            objlocation = plt.plot(obj_xyz[0][-1],obj_xyz[1][-1], markerfacecolor=color_marker,markeredgecolor=color_marker, marker='o')
            if "barycenter" in obj.capitalize():
                label = obj.capitalize().replace(" barycenter", "")
            else:
                label = obj.capitalize()
            if "-moon" in label.capitalize():
                label = label.capitalize().replace("-moon", "")

            if "Wind" in label:
                plt.text(np.array(obj_xyz[0][-1]) - 30, np.array(obj_xyz[1][-1]) + 10, f'{label}')
            else:
                plt.text(np.array(obj_xyz[0][-1]) + 10, np.array(obj_xyz[1][-1]) + 10, f'{label}')

            if plot_orbit == True:
                plt.plot(obj_xyz[0], obj_xyz[1], color=color_marker, ls='-')

        locations_simple = np.array(locations_simple)

        R, _ = cart2pol(locations_simple[:, 0], locations_simple[:, 1])
        lim_plot = np.max(R) + 20
        ax.set(xlim=(-lim_plot, lim_plot), ylim=(-lim_plot, lim_plot))


        month_strings = {
            1: 'Jan',
            2: 'Feb',
            3: 'Mar',
            4: 'Apr',
            5: 'May',
            6: 'Jun',
            7: 'Jul',
            8: 'Aug',
            9: 'Sep',
            10: 'Oct',
            11: 'Nov',
            12: 'Dec'}

        ax.set_title(f'Spacecraft Coordinates - {day} / {month_strings[month]} / {year}', fontsize=18)
        ax.set_xlabel('HEE - X / $R_{\odot}$', fontsize=14)
        ax.set_ylabel('HEE - Y / $R_{\odot}$', fontsize=14)
        plt.grid(linestyle='dashed', alpha=0.3)

        plt.show(block=False)
        return plt.gcf()

    def show_spacecraft_ids(self):
        import requests

        # Replace 'https://api.example.com' with the actual API endpoint URL
        api_url = 'https://ssd.jpl.nasa.gov/api/horizons.api?format=text&EPHEM_TYPE=VECTORS&OUT_UNITS=AU-D&COMMAND=%22spacecraft%22&CENTER=%27500%4010%27&CSV_FORMAT=%22YES%22&REF_PLANE=ECLIPTIC&REF_SYSTEM=ICRF&TP_TYPE=ABSOLUTE&VEC_LABELS=YES&VEC_CORR=%22NONE%22&VEC_DELTA_T=NO&OBJ_DATA=YES&TLIST=2460287.169281204'

        try:
            # Make a GET request to the API
            response = requests.get(api_url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Print the API response content
                print(response.text)
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"An error occurred: {e}")


    def get_all_object_ids(self):
        import requests
        # URL for the Horizons API
        horizons_url = "https://ssd.jpl.nasa.gov/horizons_batch.cgi"

        # Parameters for the API request
        params = {
            'batch': '1',  # One-time request
            'COMMAND': "'*'",  # '*' selects all objects
            'MAKE_EPHEM': 'YES',  # Generate ephemerides
            'TABLE_TYPE': 'VECTORS',
            'OUT_UNITS': 'AU-D',
            'REF_PLANE': 'ECLIPTIC',
            'REF_SYSTEM': 'J2000',
            'VEC_LABELS': 'YES',  # Include vector labels
            'CSV_FORMAT': 'YES'  # Output in CSV format
        }

        # Make the API request
        response = requests.get(horizons_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Split the response into lines and extract object IDs from CSV
            lines = response.text.split('\n')
            object_ids = [line.split(',')[0].strip() for line in lines[5:-1]]
            print("Object IDs:")
            for obj_id in object_ids:
                print(obj_id)

            return object_ids
        else:
            print(f"Error: {response.status_code}")
            return None


if __name__ == '__main__':

    # #########################
    # SETINGS
    # #########################

    if len(sys.argv)>1:
        #command line arguments.
        print(sys.argv[0])
        day = int(sys.argv[1])
        month = int(sys.argv[2])
        year = int(sys.argv[3])
    else:
        #manual day
        day = 11
        month = 7
        year = 2012

    # plot orbits? 1=yes 0=no
    plot_orbit = 1

    objects = ['sun', 'mars express', 'earth', 'venus', 'psp', 'solo', 'tesla']
    objects = ['sun',  'mercury', 'venus', 'Earth', 'wind', 'stereo-a', 'stereo-b']

    locations=[]
    # Constants
    r_sun = R_sun.value  # km
    AU = au.value  # km

    # Generate map
    solarsystem = get_HEE_coord(date=[year, month, day], objects=objects, orbitlength=50, timeres=24)

    # gives the location of the objects at the specified DATE without orbits or labels.
    stations_rsun = np.array(solarsystem.locate_simple())

    # Plotting map of objects
    figure = solarsystem.plot()

    # Verbose version of coordinates with orbit, with labels. the last position is the specified date.
    coordinates = solarsystem.locate()

    # solarsystem = get_sc_coord(date=[year, month, day], objects=objects, orbitlength=50, timeres=24)
    # # gives the location of the objects at the specified DATE without orbits or labels.
    # stations_rsun = np.array(solarsystem.locate_simple())
    #
    # # Plotting map of objects
    # figure = solarsystem.plot()
    #
    # # Verbose version of coordinates with orbit, with labels. the last position is the specified date.
    # coordinates = solarsystem.locate()
