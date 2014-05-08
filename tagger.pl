#!/usr/bin/perl -w

my @sections;
my @words;
my $prev_word;
#my $c=0;
my $compound;
my @keywords = ('invent', 'treat', 'compound', 'method');
my $key_found;
my $part_of_comp;

open (MYFILE, 'matched_patents_final_xl_edit.txt');
#open (MYFILE, 'trial.txt');
while (<MYFILE>) {
    chomp;
    #print "\n\n$_\n";
    @sections = split("\t", $_);
    $c = 0;
    $key_found = '';
    foreach my $section(@sections)
    {
        $c+=1;
        #if ($c == 2){
        #    print "Found in Title: ";
        #}
        #if ($c == 3){
        #     print "Found in Abstract: ";
        #}
        @words = split(" ", $section);
        foreach my $word (@words)
        {
            $word =~ s/^[.?,"](.*)/$1/g;
            $word =~ s/(.*)[.?,"]$/$1/g;
            if ($part_of_comp){
                $part_of_comp = "$part_of_comp $word";
            }
            ####finding compounds
            if ($word =~ /acid/)
            {
                #print "COMPOUND: $prev_word $word\n";
                print "$prev_word $word\n";
            }
            elsif ($compound){
                #print "\n COMPOUND: $compound\n";
                print "$compound\n";
                $compound = 0;
                $part_of_comp = 0;
            }
            ###example: 1',4'-Dihydro-1-methyl-spiro [piperidine and pyrrolidine-2,3'(2'H)quinoline]-2'-one
            #1',4'-Dihydro-1-methyl-spiro[piperidine and pyrolidine-2,3'(2'H)quinoline]
            #3,3′-diindolylmethane
            if ($word =~ /[1-9'′]\-[\(\[a-zA-Z]/){
                if (($word =~ /[\{\(\[]/) && ($word !~ /[\}\)\]]/)){
                    $compound = 0;
                    $part_of_comp = $word;
                }
                else{
                    $compound = $word;
                }
            }
             
            if ($word =~ /[a-zA-Z]\-[1-9'′]/){
                if (($word =~ /[\{\(\[]/) && ($word !~ /[\}\)\]]/)){
                    $compound = 0;
                    $part_of_comp = $word;
                }
                else{
                    $compound = $word;
                }
            }
            
            if ($part_of_comp && ($word =~ /[\}\]\)]/)){
                $compound = $part_of_comp;
                $part_of_comp = 0;
            }
            if ($word =~ /[nt]ol$/)
            {
                $compound = $word;
            }
            $prev_word = $word;

            ####finding type of compound
            #foreach my $keyword(@keywords){
            #    if ($word =~ /$keyword/)
            #    {
            #       $key_found .= "$word\n";            
            #    }
            #}
        }
       #print "\nKEYWORDS FOUND: $key_found\n";
       #print "$key_found\n";
    }
}
close (MYFILE); 
