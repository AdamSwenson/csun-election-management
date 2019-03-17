"""
Created by adam on 3/16/19
"""
__author__ = 'adam'

import pandas as pd
from IPython.display import display, Latex
from matplotlib import pyplot as plt
import counter.environment as env


def show_table( frame_or_series ):
    """Used to display any generic data frame or series in latex"""
    display( Latex( frame_or_series.to_latex() ) )


def show_results_tables( results ):
    for r in results:
        out = """\\begin{figure}
        \\caption{%s}
        %s
        \\end{figure}""" % (r.officeName, r.combined_results_frame.T.to_latex())
        display( Latex( out ) )


def plot_results( results, figsize=(17, 25) ):
    #     n = round(len(results)/2)
    fig, axes = plt.subplots( nrows=len( results ), ncols=2, figsize=figsize )
    row = 0;
    col = 0
    for r in results:
        r.vote_counts.plot( kind='barh', title=r.officeName, ax=axes[ row, 0 ] )
        axes[ row, 0 ].set_xlabel( "Vote count" )
        r.percentages_of_valid.plot( kind='barh', title=r.officeName + "-- Percentage of total valid votes",
                                     ax=axes[ row, 1 ] )
        axes[ row, 1 ].set_xlabel( "%" )
        row += 1
    fig.tight_layout()


# ------------------------- Abstentions

def plot_abstentions( results, figsize=(8, 5) ):
    d = [ ]
    for r in results:
        d.append( { r.officeName: r.number_abstentions } )
    abst = pd.DataFrame( d )
    fig, axes = plt.subplots( figsize=figsize )
    abst.T.plot( kind='barh', title='Abstentions', ax=axes )
    axes.get_legend().remove()
    # axes.legend(loc=9, ncol=7, mode='expand', borderaxespad=0.)
    axes.set_xlabel( "Count" )
    fig.tight_layout()


def show_abstentions_tables( results ):
    d = [ ]
    for r in results:
        d.append( { r.officeName: r.number_abstentions } )
    abst = pd.DataFrame( d )
    display( Latex( abst.to_latex() ) )


# ----------------------- Votes cast
def compute_cast( results ):
    """Determines the number of votes cast in results object"""
    cast = [ ]
    for r in results:
        cast.append( { r.officeName: r.cast_votes } )
    return pd.DataFrame( cast )


def show_cast_table( results ):
    cast = compute_cast( results )
    display( Latex( cast.to_latex() ) )


def plot_cast( results ):
    cast = compute_cast( results )
    fig, axes = plt.subplots( figsize=(8, 5) )
    cast.T.plot( kind='barh', title='Total votes cast', ax=axes )
    axes.get_legend().remove()
    axes.set_xlabel( "Count" )
    fig.tight_layout()


# ---------------- Daily marginal
def compute_daily_marginal( data ):
    """This requires the original data frame containing
    the imported results. It is not run off of the list
    of processed results objects"""
    d = data.copy( deep=True )
    d.set_index( 'RecordedDate', inplace=True )
    return d.resample( 'D' )[ 'ResponseId' ].count()


def show_daily_marginal_table( data ):
    m = compute_daily_marginal( data )
    display( Latex( m.T.to_latex() ) )


def plot_daily_marginal( data, figsize=(7, 5) ):
    d = compute_daily_marginal( data )
    #     d= results.copy(deep=True)
    #     d.set_index('RecordedDate', inplace=True)
    fig, axes = plt.subplots( figsize=figsize )
    d.plot( kind='bar', ax=axes )
    axes.set_ylabel( '# votes' );
    axes.set_title( "Daily marginal votes" );
    axes.set_xlabel( 'Date' )
    # Adjust the formating of the dates in the x axis
    xtl = [ item.get_text()[ :10 ] for item in axes.get_xticklabels() ]
    _ = axes.set_xticklabels( xtl )
    # rotate and align the tick labels so they look better
    fig.autofmt_xdate()
    fig.tight_layout()


def load_eligibility( filepath=env.ELIGIBILITY_FILE_PATH ):
    eligible = pd.read_excel( filepath )
    eligible.set_index( 'year', inplace=True )
    return eligible


def load_past_returns( election_type, filepath=env.PAST_RETURNS_FILE_PATH ):
    """Imports returns from the relevant sheet
    election_type should be either 'senate' or 'general'
    """
    sheet = "Data-{}".format( election_type.lower() )
    #     sheet = 'Data-senate' if election_type == 'senate' else 'Data-general'
    pastData = pd.read_excel( filepath, sheet_name=sheet )
    pastData.set_index( 'Year', inplace=True )
    return pastData


def update_returns( frame_w_timestamp_index, election_type, year, save=False, filepath=env.PAST_RETURNS_FILE_PATH ):
    """Adds the daily cumulative sum of vote counts for the presesnt year to the
    data for past years"""
    past = load_past_returns( election_type )
    # Calcluate marginal votes for present year and add
    i = 0
    for v in frame_w_timestamp_index.resample( 'D' )[ 'ResponseId' ].count().cumsum():
        past.loc[ year, past.columns[ i ] ] = v
        i += 1
    if save:
        sheet = "Data-{}".format( election_type.lower() )
        past.to_excel( filepath, sheet_name=sheet )
    return past


def compute_daily_cumulative( data ):
    """Returns the cumulative sum of votes cast on
    each day of the election.
    This requires the original data frame containing
    the imported results. It is not run off of the list
    of processed results objects"""
    d = data.copy( deep=True )
    d.set_index( 'RecordedDate', inplace=True )
    return d.resample( 'D' )[ 'ResponseId' ].count().cumsum()


def calc_proport_of_eligible( frame, year, total ):
    numEligible = frame.loc[ year ]
    return total / numEligible


def plot_returns( returns, returns_proport, election_type, figsize=(20, 8) ):
    t = "{} election".format( election_type )
    # t = "General election"
    fig, axes = plt.subplots( nrows=2, figsize=figsize )
    returns.T.plot( ax=axes[ 0 ] )
    axes[ 0 ].set_title( "%s -- total votes" % t )
    axes[ 0 ].set_ylabel( "Total votes cast" );
    axes[ 0 ].set_xlabel( "Day in election period" )
    returns_proport.T.plot( ax=axes[ 1 ] )
    axes[ 1 ].set_title( "{} returns -- proportion of eligible voters".format( t ) )
    axes[ 1 ].set_ylabel( "# eligible voters / total votes" );
    axes[ 1 ].set_xlabel( "Day in election period" )
    fig.tight_layout()


def plot_cumulative_votes( returns, election_type, figsize=(8, 4) ):
    t = "{} election".format( election_type )
    fig, axes = plt.subplots( figsize=figsize )
    returns.T.plot( ax=axes )
    axes.set_title( "%s -- total votes" % t )
    axes.set_ylabel( "Total votes cast" );
    axes.set_xlabel( "Day in election period" )
    fig.tight_layout()


def plot_proportion_returns( returns_proport, election_type, figsize=(8, 4) ):
    t = "{} election".format( election_type )
    fig, axes = plt.subplots( figsize=figsize )
    returns_proport.T.plot( ax=axes )
    axes.set_title( "{} returns -- proportion of eligible senate voters".format( t ) )
    axes.set_ylabel( "# eligible voters / total votes" );
    axes.set_xlabel( "Day in election period" )
    fig.tight_layout()


if __name__ == '__main__':
    pass
