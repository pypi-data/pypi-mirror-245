# Tools
SAMTOOLS_STATS = 'samtools_stats'
BAMSTATS = 'bamstats'
RNASEQQC = 'rnaseqqc'
PICARD_COLLECT_ALIGNMENT_SUMMARY_METRICS = 'picard_CollectAlignmentSummaryMetrics'
PICARD_COLLECT_INSERT_SIZE_METRICS = 'picard_CollectInsertSizeMetrics'
PICARD_COLLECT_WGS_METRICS = 'picard_CollectWgsMetrics'
FASTQC = 'fastqc'


########################################################################
# Metrics to extract for each tool
########################################################################
samtools_stats_metrics = {
    'raw total sequences': {
        'key': 'Total Sequences [Samtools]',
        'tooltip': 'Total number of reads in a file, excluding supplementary and secondary reads',
        'type': int
    },
    'sequences': {
        'key': 'Processed Sequences [Samtools]',
        'tooltip': 'Number of processed reads',
        'type': int
    },
    '1st fragments': {
        'key': '1st Fragments [Samtools]',
        'tooltip': 'Number of first fragment reads',
        'type': int
    },
    'last fragments': {
        'key': 'Last Fragments [Samtools]',
        'tooltip': 'Number of last fragment reads',
        'type': int
    },
    'reads paired': {
        'key': 'Reads Paired [Samtools]',
        'tooltip': 'Number of paired reads, mapped or unmapped, that are neither secondary nor supplementary (paired-end technology bit set)',
        'type': int
    },
    'reads mapped': {
        'key': 'Reads Mapped [Samtools]',
        'tooltip': 'Number of reads, paired or single, that are mapped',
        'type': int
    },
    'reads mapped and paired': {
        'key': 'Reads Mapped and Paired [Samtools]',
        'tooltip': 'Number of mapped paired reads (paired-end technology bit set with both mates mapped)',
        'type': int
    },
    'reads properly paired': {
        'key': 'Reads Properly Paired [Samtools]',
        'tooltip': 'Number of mapped paired reads (proper-pair bit set, both mates mapped within the expected distance)',
        'type': int
    },
    'reads unmapped': {
        'key': 'Reads Unmapped [Samtools]',
        'tooltip': 'Number of unmapped reads',
        'type': int
    },
    'reads duplicated': {
        'key': 'Reads Duplicated [Samtools]',
        'tooltip': 'Number of duplicate reads',
        'type': int
    },
    'reads MQ0': {
        'key': 'Reads MQ0 [Samtools]',
        'tooltip': 'Number of mapped reads with mapping quality 0',
        'type': int
    },
    'reads QC failed': {
        'key': 'Reads QC-Failed [Samtools]',
        'tooltip': 'Number of reads that failed the quality checks',
        'type': int
    },
    'non-primary alignments': {
        'key': 'Non-Primary Alignments [Samtools]',
        'tooltip': 'Number of secondary reads',
        'type': int
    },
    'supplementary alignments': {
        'key': 'Supplementary Alignments [Samtools]',
        'tooltip': 'Number of supplementary reads',
        'type': int
    },
    'pairs on different chromosomes': {
        'key': 'Pairs on Different Chromosomes [Samtools]',
        'tooltip': 'Number of pairs where one read is on one chromosome and the mate read is on a different chromosome',
        'type': int
    },
    'percentage of properly paired reads (%)': {
        'key': 'Percentage of Properly Paired Reads [Samtools]',
        'tooltip': None,
        'type': float
    },
}

picard_CollectAlignmentSummaryMetrics_metrics = {
    'PF_ALIGNED_BASES': {
        'key': 'Aligned Bases [Picard]',
        'tooltip': 'The total number of aligned bases',
        'type': int
    },
    'PF_HQ_ALIGNED_BASES': {
        'key': 'Aligned Bases (High Quality) [Picard]',
        'tooltip': 'The number of aligned bases in reads that were mapped at high quality',
        'type': int
    },
    'PF_MISMATCH_RATE': {
        'key': 'Aligned Bases Mismatch Rate [Picard]',
        'tooltip': 'The fraction of bases mismatching the reference for all aligned bases',
        'type': float
    },
    'PF_HQ_ERROR_RATE': {
        'key': 'Aligned Bases Mismatch Rate (High Quality) [Picard]',
        'tooltip': 'The fraction of bases mismatching the reference in reads that were mapped at high quality',
        'type': float
    },
    'PF_INDEL_RATE': {
        'key': 'Indel Rate [Picard]',
        'tooltip':  'The number of insertion and deletion events per 100 aligned bases',
        'type': float
    },
    'MEAN_READ_LENGTH': {
        'key': 'Mean Read Length [Picard]',
        'tooltip': 'The mean length of the set of reads examined',
        'type': int
    },
    'SD_READ_LENGTH': {
        'key': 'Read Length Standard Deviation [Picard]',
        'tooltip': 'The standard deviation for the length of the set of reads examined',
        'type': int
    },
}

picard_CollectInsertSizeMetrics_metrics = {
    # [5]
    'MEAN_INSERT_SIZE': {
        'key': 'Mean Insert Size',
        'tooltip': 'The mean insert size for the pair orientation',
        'type': float
    },
    # [6]
    'STANDARD_DEVIATION': {
        'key': 'Insert Size Standard Deviation',
        'tooltip': 'Standard deviation of insert sizes for the pair orientation',
        'type': float
    },
    # [7]
    'READ_PAIRS': {
        'key': 'Total Number of Read Pairs',
        'tooltip': 'The total number of read pairs that were examined for the pair orientation',
        'type': int
    },
    # 'PAIR_ORIENTATION' [8]
}

picard_CollectWgsMetrics_metrics = {
    'GENOME_TERRITORY': {
        'key': 'Effective Genome Size [Picard]',
        'tooltip': 'The number of non-N bases in the genome',
        'type': int
    },
    'MEAN_COVERAGE': {
        'key': 'Mean Coverage [Picard]',
        'tooltip': 'The mean coverage of the genome',
        'type': float
    },
    'SD_COVERAGE': {
        'key': 'Coverage Standard Deviation [Picard]',
        'tooltip': 'The standard deviation for the coverage',
        'type': float
    },
}

bamstats_metrics = {
    'Estimate_Average_Coverage': {
        'key': 'Average coverage (estimated)',
        'tooltip': 'Estimated average coverage',
        'type': float
    }
}

rnaseqqc_metrics = {
    "3' bias MAD_Std": {
        'key': "3' bias MAD_Std",
        'tooltip': "3' Bias statistics (Mean, Median, Std Deviation, Median Absolute Deviation, 25th percentile, 75th percentile): These aggregate statistics are based on the total coverage in 100 bp windows on both the 3' and 5' ends of a gene. The windows are both offset 150 bases into the gene. This computation is only performed on genes at least 600bp long and with at least 5 unambiguous reads. A gene with even coverage in both it's 3' and 5' windows would have a bias of 0.5; bias near 1 or 0 may indicate degredation",
        'type': float
    },
    "3' bias Std": {
        'key': "3' bias Std",
        'tooltip': "3' Bias statistics (Mean, Median, Std Deviation, Median Absolute Deviation, 25th percentile, 75th percentile): These aggregate statistics are based on the total coverage in 100 bp windows on both the 3' and 5' ends of a gene. The windows are both offset 150 bases into the gene. This computation is only performed on genes at least 600bp long and with at least 5 unambiguous reads. A gene with even coverage in both it's 3' and 5' windows would have a bias of 0.5; bias near 1 or 0 may indicate degredation",
        'type': float
    },
    "3' Bias, 25th Percentile": {
        'key': "3' Bias, 25th Percentile",
        'tooltip': "3' Bias statistics (Mean, Median, Std Deviation, Median Absolute Deviation, 25th percentile, 75th percentile): These aggregate statistics are based on the total coverage in 100 bp windows on both the 3' and 5' ends of a gene. The windows are both offset 150 bases into the gene. This computation is only performed on genes at least 600bp long and with at least 5 unambiguous reads. A gene with even coverage in both it's 3' and 5' windows would have a bias of 0.5; bias near 1 or 0 may indicate degredation",
        'type': float
    },
    "3' Bias, 75th Percentile": {
        'key': "3' Bias, 75th Percentile",
        'tooltip': "3' Bias statistics (Mean, Median, Std Deviation, Median Absolute Deviation, 25th percentile, 75th percentile): These aggregate statistics are based on the total coverage in 100 bp windows on both the 3' and 5' ends of a gene. The windows are both offset 150 bases into the gene. This computation is only performed on genes at least 600bp long and with at least 5 unambiguous reads. A gene with even coverage in both it's 3' and 5' windows would have a bias of 0.5; bias near 1 or 0 may indicate degredation",
        'type': float
    },
    "Genes used in 3' bias": {
        'key': "Genes used in 3' bias",
        'tooltip': "",
        'type': int
    },
    "Mean 3' bias": {
        'key': "Mean 3' bias",
        'tooltip': "",
        'type': float
    },
    "Median 3' bias": {
        'key': "Median 3' bias",
        'tooltip': "",
        'type': float
    },
    'Alternative Alignments': {
        'key': 'Alternative Alignments',
        'tooltip': 'Duplicate read entries providing alternative coordinates',
        'type': int
    },
    'Base Mismatch': {
        'key': 'Base Mismatch',
        'tooltip': 'The total number of mismatched bases (as determined by the "NM" tag) of all "Mapped Reads" (as defined above) divided by the total aligned length of all "Mapped Reads".',
        'type': float
    },
    'Chimeric Reads': {
        'key': 'Chimeric Reads',
        'tooltip': '',
        'type': int
    },
    'Duplicate Rate of Mapped': {
        'key': 'Duplicate Rate of Mapped',
        'tooltip': 'This is the proportion of all reads which were marked as PCR/Optical Duplicates out of all "Mapped Reads" (as defined above; excludes Secondary and Vendor QC Failed reads). This is complementary to the "Unique Rate of Mapped".',
        'type': int
    },
    'End 1 Antisense': {
        'key': 'End 1 Antisense',
        'tooltip': 'Number of reads that were sequenced in the antisense direction',
        'type': int
    },
    'End 1 Mapping Rate': {
        'key': 'End 1 Mapping Rate',
        'tooltip': 'The proportion of Paired reads which were marked as First or Second in the pair, respectively, out of all "Mapped Reads" (above).',
        'type': float
    },
    'End 1 Mismatch Rate': {
        'key': 'End 1 Mismatch Rate',
        'tooltip': 'The proportion of mismatched bases (as determined by the "NM" tag) belonging to First or Second mates, divided by the total aligned length of all "Mapped" (above) First or Second mates, respectively.',
        'type': float
    },
    'End 1 Sense': {
        'key': 'End 1 Sense',
        'tooltip': 'Number of End 1 reads that were sequenced in the sense direction',
        'type': int
    },
    'End 1 Sense Rate': {
        'key': 'End 1 Sense Rate',
        'tooltip': 'The proportion of First or Second Mate reads which intersected with a Sense Strand feature out of all First or Second Mate reads which intersected with any features, respectively.',
        'type': float
    },
    'End 2 Antisense': {
        'key': 'End 2 Antisense',
        'tooltip': 'Number of reads that were sequenced in the antisense direction',
        'type': int
    },
    'End 2 Mapping Rate': {
        'key': 'End 2 Mapping Rate',
        'tooltip': 'The proportion of Paired reads which were marked as First or Second in the pair, respectively, out of all "Mapped Reads" (above).',
        'type': float
    },
    'End 2 Mismatch Rate': {
        'key': 'End 2 Mismatch Rate',
        'tooltip': 'The proportion of mismatched bases (as determined by the "NM" tag) belonging to First or Second mates, divided by the total aligned length of all "Mapped" (above) First or Second mates, respectively.',
        'type': float
    },
    'End 2 Sense': {
        'key': 'End 2 Sense',
        'tooltip': 'Number of End 2 reads that were sequenced in the sense direction',
        'type': int
    },
    'End 2 Sense Rate': {
        'key': 'End 2 Sense Rate',
        'tooltip': 'The proportion of First or Second Mate reads which intersected with a Sense Strand feature out of all First or Second Mate reads which intersected with any features, respectively.',
        'type': float
    },
    'Estimated Library Complexity': {
        'key': 'Estimated Library Complexity',
        'tooltip': 'An estimation of the number of unique cDNA fragments present in the library. This computation follows the same formula as Picard EstimateLibraryComplexity',
        'type': int
    },
    'Exonic Rate': {
        'key': 'Exonic Rate',
        'tooltip': 'The proportion of "Mapped Reads" (above) for which all aligned segments unambiguously aligned to exons of the same gene.',
        'type': float
    },
    'Exonic/Intron ratio': {
        'key': 'Exonic/Intron ratio',
        'tooltip': 'Exonic Reads/Intronic Reads',
        'type': float
    },
    'Expression Profiling Efficiency': {
        'key': 'Expression Profiling Efficiency',
        'tooltip': 'The proportion of "Exonic Reads" (see "Exonic Rate", below) out of all reads which were not Secondary Alignments or Platform/Vendor QC Failing reads.',
        'type': float
    },
    'Exons with >0 reads': {
        'key': 'Exons with >0 reads',
        'tooltip': '',
        'type': int
    },
    'Exons with >=2 reads': {
        'key': 'Exons with >=2 reads',
        'tooltip': '',
        'type': int
    },
    'Exons with >=10 reads': {
        'key': 'Exons with >=10 reads',
        'tooltip': '',
        'type': int
    },
    'Failed Vendor QC': {
        'key': 'Failed Vendor QC',
        'tooltip': '',
        'type': int
    },
    'Genes Detected': {
        'key': 'Genes Detected',
        'tooltip': 'The number of genes which had at least 5 unambiguous reads. The detection threshold can be changed with --detection-threshold',
        'type': int
    },
    'Genes with >0 reads': {
        'key': 'Genes with >0 reads',
        'tooltip': '',
        'type': int
    },
    'Genes with >=2 reads': {
        'key': 'Genes with >=2 reads',
        'tooltip': '',
        'type': int
    },
    'Genes with >=10 reads': {
        'key': 'Genes with >=10 reads',
        'tooltip': '',
        'type': int
    },
    'Intergenic Rate': {
        'key': 'Intergenic Rate',
        'tooltip': 'The proportion of "Mapped Reads" (above) for which none of the aligned segments intersected any genes.',
        'type': float
    },
    'Intragenic Rate': {
        'key': 'Intragenic Rate',
        'tooltip': 'The sum of "Exonic" and "Intronic" rates (see "Exonic Rate" and "Intronic Rate" above)',
        'type': float
    },
    'Intronic Rate': {
        'key': 'Intronic Rate',
        'tooltip': 'The proportion of "Mapped Reads" (above) for which all aligned segments unambiguously aligned to the same gene, but none of which intersected any exons of the gene.',
        'type': float
    },
    'Mapped Reads': {
        'key': 'Mapped Reads',
        'tooltip': '',
        'type': int
    },
    'Mapped Unique Reads': {
        'key': 'Mapped Unique Reads',
        'tooltip': '',
        'type': int
    },
    'Mapping Rate': {
        'key': 'Mapping Rate',
        'tooltip': 'The proportion of all reads in the Bam which were Mapped, and not Secondary Alignments or Platform/Vendor QC Failing reads ("Mapped Reads").',
        'type': float
    },
    'Read Length': {
        'key': 'Read Length',
        'tooltip': 'The longest aligned length observed in any read',
        'type': int
    },
    'rRNA Rate': {
        'key': 'rRNA Rate',
        'tooltip': 'The proportion of "Mapped Reads" (above) which at least partially intersected with an annotated rRNA gene. This is not complementary to any other rates.',
        'type': float
    },
    'rRNA Reads': {
        'key': 'rRNA Reads',
        'tooltip': '',
        'type': int
    },
    'Total Mapped Pairs': {
        'key': 'Total Mapped Pairs',
        'tooltip': '',
        'type': int
    },
    'Total Reads': {
        'key': 'Total Reads',
        'tooltip': '',
        'type': int
    },
    'Unique Rate of Mapped': {
        'key': 'Unique Rate of Mapped',
        'tooltip': 'This is the proportion of reads which were not marked as PCR/Optical Duplicates out of all "Mapped Reads"',
        'type': float
    },
    'Unpaired Reads': {
        'key': 'Unpaired Reads',
        'tooltip': '',
        'type': int
    },

}

fastqc_metrics = {
    'Basic Statistics': {
        'key': 'Basic Statistics',
        'tooltip': '',
        'type': str
    },
    'Per base sequence quality': {
        'key': 'Per base sequence quality',
        'tooltip': '',
        'type': str
    },
    'Per tile sequence quality': {
        'key': 'Per tile sequence quality',
        'tooltip': '',
        'type': str
    },
    'Per sequence quality scores': {
        'key': 'Per sequence quality scores',
        'tooltip': '',
        'type': str
    },
    'Per base sequence content': {
        'key': 'Per base sequence content',
        'tooltip': '',
        'type': str
    },
    'Per sequence GC content': {
        'key': 'Per sequence GC content',
        'tooltip': '',
        'type': str
    },
    'Per base N content': {
        'key': 'Per base N content',
        'tooltip': '',
        'type': str
    },
    'Sequence Length Distribution': {
        'key': 'Sequence Length Distribution',
        'tooltip': '',
        'type': str
    },
    'Sequence Duplication Levels': {
        'key': 'Sequence Duplication Levels',
        'tooltip': '',
        'type': str
    },
    'Overrepresented sequences': {
        'key': 'Overrepresented sequences',
        'tooltip': '',
        'type': str
    },
    'Adapter Content': {
        'key': 'Adapter Content',
        'tooltip': '',
        'type': str
    }
}


metrics = {
    SAMTOOLS_STATS: samtools_stats_metrics,
    BAMSTATS: bamstats_metrics,
    RNASEQQC: rnaseqqc_metrics,
    PICARD_COLLECT_ALIGNMENT_SUMMARY_METRICS: picard_CollectAlignmentSummaryMetrics_metrics,
    PICARD_COLLECT_INSERT_SIZE_METRICS: picard_CollectInsertSizeMetrics_metrics,
    PICARD_COLLECT_WGS_METRICS: picard_CollectWgsMetrics_metrics,
    FASTQC: fastqc_metrics
}
